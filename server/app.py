import json
import os
import re
import socket
import urllib.parse
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_file
import requests

app = Flask(__name__)

@app.route("/download/ccwifi-bridge.tar.gz")
def download_package():
    pkg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ccwifi-bridge.tar.gz")
    if os.path.exists(pkg_path):
        return send_file(pkg_path, as_attachment=True, download_name="ccwifi-bridge.tar.gz")
    return "Package not found", 404

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    default_cfg = {
        "radio_ip": "192.168.1.141",
        "radio_user": "admin",
        "radio_pass": "admin",
        "port": 5000
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                default_cfg.update(data)
        except Exception as e:
            print("Warning loading config.json:", e)
    return default_cfg

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print("Warning saving config.json:", e)

_cfg = load_config()
RADIO_IP = os.environ.get("RADIO_IP", _cfg.get("radio_ip", "192.168.1.141"))
RADIO_USER = _cfg.get("radio_user", "admin")
RADIO_PASS = _cfg.get("radio_pass", "admin")
SERVER_PORT = int(os.environ.get("PORT", _cfg.get("port", 5000)))

# Radio-Browser API Mirrors for reliability
RADIO_BROWSER_MIRRORS = [
    "https://de1.api.radio-browser.info",
    "https://nl1.api.radio-browser.info",
    "https://at1.api.radio-browser.info"
]

def discover_reciva_radio(timeout=2.0):
    """Broadcasts SSDP M-SEARCH to automatically locate Reciva/Sharpfin radio on LAN."""
    msg = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST: 239.255.255.250:1900\r\n"
        'MAN: "ssdp:discover"\r\n'
        "MX: 2\r\n"
        "ST: ssdp:all\r\n\r\n"
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(timeout)
    found_ips = []
    try:
        s.sendto(msg.encode(), ("239.255.255.250", 1900))
        while True:
            data, addr = s.recvfrom(2048)
            text = data.decode("utf-8", errors="ignore")
            if "reciva" in text.lower() or "sharpfin" in text.lower():
                ip = addr[0]
                if ip not in found_ips:
                    found_ips.append(ip)
    except Exception:
        pass
    finally:
        s.close()
    
    # Verify candidate IPs on port 23 or 80
    for ip in found_ips:
        for p in (23, 80):
            try:
                test_s = socket.create_connection((ip, p), timeout=1.0)
                test_s.close()
                return ip
            except Exception:
                pass
    return None

def get_local_ip():
    """Detect LAN IP of the server machine to construct proxy URLs for the radio."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((RADIO_IP, 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def send_telnet_commands(commands, timeout=5):
    """Executes commands on the radio using pure sockets (compatible with Python 3.13/3.14+)."""
    global RADIO_IP
    try:
        s = socket.create_connection((RADIO_IP, 23), timeout=timeout)
        s.settimeout(timeout)

        def read_until(pattern):
            buf = b""
            while pattern not in buf:
                chunk = s.recv(1024)
                if not chunk:
                    break
                buf += chunk
            return buf.decode('ascii', errors='ignore')

        read_until(b"login:")
        s.sendall(RADIO_USER.encode('ascii') + b"\n")
        read_until(b"Password:")
        s.sendall(RADIO_PASS.encode('ascii') + b"\n")
        read_until(b"#")

        output = []
        for cmd in commands:
            s.sendall(cmd.encode('ascii') + b"\n")
            res = read_until(b"#")
            output.append(res)

        s.sendall(b"exit\n")
        s.close()
        return True, "\n".join(output)
    except Exception as e:
        return False, str(e)

@app.route("/")
def index():
    return render_template("index.html", radio_ip=RADIO_IP, server_ip=get_local_ip(), server_port=SERVER_PORT)

@app.route("/api/status")
def radio_status():
    """Check if radio is online and reachable, with auto-discovery fallback."""
    global RADIO_IP
    is_online = False
    for port in (23, 80):
        try:
            s = socket.create_connection((RADIO_IP, port), timeout=1.2)
            s.close()
            is_online = True
            break
        except Exception:
            pass
    
    # If offline, attempt SSDP auto-discovery to see if radio moved IPs
    if not is_online:
        discovered = discover_reciva_radio(timeout=1.5)
        if discovered and discovered != RADIO_IP:
            print(f"Auto-discovered radio at new IP: {discovered} (was {RADIO_IP})")
            RADIO_IP = discovered
            cfg = load_config()
            cfg["radio_ip"] = discovered
            save_config(cfg)
            is_online = True

    return jsonify({
        "radio_ip": RADIO_IP,
        "online": is_online,
        "server_ip": get_local_ip(),
        "server_port": SERVER_PORT
    })

@app.route("/api/settings", methods=["GET", "POST"])
def radio_settings():
    """Get or update current radio connection settings."""
    global RADIO_IP
    if request.method == "POST":
        data = request.json or {}
        new_ip = data.get("radio_ip", "").strip()
        if not new_ip:
            return jsonify({"success": False, "error": "IP address is required"}), 400
        
        # Test connectivity
        reachable = False
        for port in (23, 80):
            try:
                s = socket.create_connection((new_ip, port), timeout=2.0)
                s.close()
                reachable = True
                break
            except Exception:
                pass
        
        if not reachable:
            return jsonify({"success": False, "error": f"Could not reach radio at {new_ip} on port 23 or 80. Check IP and Wi-Fi connection."}), 400
        
        RADIO_IP = new_ip
        cfg = load_config()
        cfg["radio_ip"] = new_ip
        save_config(cfg)
        return jsonify({"success": True, "radio_ip": RADIO_IP, "online": True})
    
    return jsonify({
        "radio_ip": RADIO_IP,
        "server_ip": get_local_ip(),
        "server_port": SERVER_PORT
    })

@app.route("/api/radio/discover", methods=["POST"])
def radio_discover():
    """Force run SSDP discovery to auto-locate radio on LAN."""
    global RADIO_IP
    found_ip = discover_reciva_radio(timeout=2.5)
    if found_ip:
        RADIO_IP = found_ip
        cfg = load_config()
        cfg["radio_ip"] = found_ip
        save_config(cfg)
        return jsonify({"success": True, "radio_ip": found_ip, "message": f"Found Reciva Radio at {found_ip}"})
    return jsonify({"success": False, "error": "Could not auto-detect radio via SSDP. Please enter IP manually."}), 404


MAX_PRESETS = 40

@app.route("/api/presets")
def get_presets():
    """Reads Presets 1-40 directly from radio files in a single fast command."""
    presets = [{"id": i, "name": "[Empty]", "url": ""} for i in range(1, MAX_PRESETS + 1)]
    
    # Read all preset XML files in one quick command
    success, raw_out = send_telnet_commands(["head -n 25 /root/config/preset*.xml 2>/dev/null"])

    if success and raw_out:
        # Match sections like ==> /root/config/preset1.xml <== ... <preset ...>...</preset>
        blocks = re.findall(r'preset(\d+)\.xml.*?<preset[^>]*>(.*?)</preset>', raw_out, re.DOTALL)
        for pid_str, content in blocks:
            try:
                pid = int(pid_str)
                if 1 <= pid <= MAX_PRESETS:
                    title_m = re.search(r'<title>(.*?)</title>', content)
                    url_m = re.search(r'<url>(.*?)</url>', content)
                    title = title_m.group(1).strip() if title_m else ""
                    url = url_m.group(1).strip() if url_m else ""
                    presets[pid - 1] = {
                        "id": pid,
                        "name": title if title else f"Preset {pid}",
                        "url": url
                    }
            except Exception:
                pass

    return jsonify(presets)

@app.route("/api/presets/clear", methods=["POST"])
def clear_preset():
    """Clears/deletes a preset slot from the radio."""
    preset_id = int((request.json or {}).get("preset", 1))
    if not (1 <= preset_id <= MAX_PRESETS):
        return jsonify({"success": False, "error": "Invalid preset number"}), 400

    cmds = [
        "mount / -orw,remount",
        f"rm -f /root/config/preset{preset_id}.xml",
        "sync; mount / -oro,remount"
    ]
    success, out = send_telnet_commands(cmds)
    if not success:
        return jsonify({"success": False, "error": out}), 500
    return jsonify({"success": True, "preset": preset_id})

@app.route("/api/presets/assign", methods=["POST"])
def assign_preset():
    """
    Assigns a station URL to a preset on the radio.
    If the stream is HTTPS, automatically wraps it in our local HTTP bridge proxy!
    """
    data = request.json or {}
    preset_id = int(data.get("preset", 1))
    name = data.get("name", f"Station {preset_id}").strip()
    original_url = data.get("url", "").strip()

    if not original_url:
        return jsonify({"success": False, "error": "URL is required"}), 400

    clean_name = name.replace("&", "and").replace("<", "").replace(">", "").replace("'", "")

    if original_url.startswith("https://") or ("&" in original_url) or ("?" in original_url):
        local_ip = get_local_ip()
        encoded = urllib.parse.quote(original_url, safe='')
        target_url = f"http://{local_ip}:{SERVER_PORT}/stream?url={encoded}"
    else:
        target_url = original_url

    xml_content = f"<preset type='PresetType:Internet' id='{preset_id}'><station id='3508'><data><stream><url>{target_url}</url><title>{clean_name}</title></stream></data></station></preset>"

    cmds = [
        "mount / -orw,remount",
        f"echo \"{xml_content}\" > /root/config/preset{preset_id}.xml",
        "sync; mount / -oro,remount"
    ]
    success, out = send_telnet_commands(cmds)

    if not success:
        return jsonify({"success": False, "error": f"Failed writing to radio: {out}"}), 500

    auto_play = data.get("play_now", True)
    if auto_play:
        try:
            requests.get(f"http://{RADIO_IP}/cgi-bin/Presets_play.cgi?i={preset_id}", timeout=3)
        except Exception:
            pass

    return jsonify({
        "success": True,
        "preset": preset_id,
        "name": clean_name,
        "url": target_url,
        "original_url": original_url,
        "bridged": target_url != original_url
    })

@app.route("/api/radio/play", methods=["POST"])
def play_preset():
    """Tells radio to start playing a preset number."""
    preset_id = request.json.get("preset", 1)
    try:
        requests.get(f"http://{RADIO_IP}/cgi-bin/Presets_play.cgi?i={preset_id}", timeout=3)
        return jsonify({"success": True, "preset": preset_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/search")
def search_stations():
    """Search stations by artist, title, tag, or country using Radio-Browser API."""
    query = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()
    country = request.args.get("country", "").strip()
    limit = int(request.args.get("limit", 20))
    page = int(request.args.get("page", 1))
    offset = (page - 1) * limit

    results = []
    for mirror in RADIO_BROWSER_MIRRORS:
        try:
            params = {
                "limit": limit,
                "offset": offset,
                "order": "votes",
                "reverse": "true",
                "hidebroken": "true"
            }
            if query:
                params["name"] = query
            if tag:
                params["tag"] = tag
            if country:
                params["countrycode"] = country

            url = f"{mirror}/json/stations/search"
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                raw_stations = resp.json()
                for s in raw_stations:
                    stream_url = s.get("url_resolved") or s.get("url")
                    if not stream_url:
                        continue
                    results.append({
                        "id": s.get("stationuuid"),
                        "name": s.get("name", "Unknown"),
                        "url": stream_url,
                        "favicon": s.get("favicon", ""),
                        "tags": s.get("tags", ""),
                        "country": s.get("country", ""),
                        "codec": s.get("codec", "MP3"),
                        "bitrate": s.get("bitrate", 128),
                        "votes": s.get("votes", 0)
                    })
                break
        except Exception:
            continue

    return jsonify({
        "page": page,
        "limit": limit,
        "count": len(results),
        "results": results
    })

@app.route("/api/podcasts")
def search_podcasts():
    """Search podcasts via Apple iTunes Search API."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": []})

    url = "https://itunes.apple.com/search"
    params = {
        "term": query,
        "entity": "podcast",
        "limit": 15
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
        results = []
        for p in data.get("results", []):
            results.append({
                "id": str(p.get("collectionId")),
                "name": p.get("collectionName"),
                "artist": p.get("artistName"),
                "feed_url": p.get("feedUrl"),
                "artwork": p.get("artworkUrl600") or p.get("artworkUrl100"),
                "genres": p.get("genres", [])
            })
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e), "results": []}), 500

@app.route("/api/podcasts/latest")
def get_latest_podcast_episode():
    """Fetches the latest episode stream URL from a podcast RSS feed."""
    feed_url = request.args.get("feed", "").strip()
    if not feed_url:
        return jsonify({"error": "feed URL required"}), 400

    try:
        r = requests.get(feed_url, timeout=7, headers={"User-Agent": "SmartRadioBridge/1.0"})
        root = ET.fromstring(r.content)
        item = root.find(".//item")
        if item is not None:
            title = item.findtext("title") or "Latest Episode"
            enclosure = item.find("enclosure")
            if enclosure is not None and enclosure.get("url"):
                return jsonify({
                    "title": title,
                    "stream_url": enclosure.get("url"),
                    "type": enclosure.get("type", "audio/mpeg")
                })
        return jsonify({"error": "No playable audio episode found in feed"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stream")
def stream_bridge():
    """
    Transparent HTTP Audio Stream Bridge:
    Proxies external modern HTTPS / dynamic streams as plain HTTP for the CC WiFi!
    """
    target_url = request.args.get("url", "").strip()
    if not target_url:
        return "Target stream URL is required", 400

    headers = {
        "User-Agent": "Reciva/1.0 (CC WiFi Radio Bridge)",
        "Icy-MetaData": "1"
    }

    try:
        req = requests.get(target_url, stream=True, timeout=10, headers=headers)

        def generate():
            for chunk in req.iter_content(chunk_size=4096):
                if chunk:
                    yield chunk

        resp_headers = {
            "Content-Type": req.headers.get("Content-Type", "audio/mpeg"),
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Server": "SmartRadioBridge/1.0"
        }
        if "icy-name" in req.headers:
            resp_headers["icy-name"] = req.headers["icy-name"]

        return Response(stream_with_context(generate()), headers=resp_headers)
    except Exception as e:
        return f"Stream Bridge Error: {e}", 502

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("==================================================")
    print(" CC WiFi Smart Radio Bridge Server")
    print(f" Target Radio IP:  {RADIO_IP}")
    print(f" Local Web UI:     http://localhost:{SERVER_PORT}")
    print(f" Network Web UI:   http://{local_ip}:{SERVER_PORT}")
    print("==================================================")
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)
