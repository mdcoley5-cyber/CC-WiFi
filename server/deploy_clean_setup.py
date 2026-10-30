import socket
import threading
import time
from app import send_telnet_commands, get_local_ip

def upload_file(local_path, remote_path):
    local_ip = get_local_ip()
    port = 9997
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", port))
    server_sock.listen(1)

    with open(local_path, "rb") as f:
        data = f.read()

    def trigger():
        time.sleep(0.3)
        send_telnet_commands([f"nc {local_ip} {port} > {remote_path}"])

    t = threading.Thread(target=trigger)
    t.start()
    conn, addr = server_sock.accept()
    conn.sendall(data)
    conn.close()
    server_sock.close()
    t.join()
    print(f"Uploaded {local_path} -> {remote_path} ({len(data)} bytes)")

print("=== DEPLOYING CLEAN CONFIG & PRESET NAVIGATION ===")
print("Uploading clean_SLR_TopLevelMenuCache.xml...")
upload_file("clean_SLR_TopLevelMenuCache.xml", "/tmp/clean_menu.xml")

print("Uploading clean_config622.txt...")
upload_file("clean_config622.txt", "/tmp/clean_cfg.txt")

# Deploy on radio
cmds = [
    "cp /tmp/clean_menu.xml /mnt/config/SLR_TopLevelMenuCache.xml",
    "mount / -orw,remount",
    "cp /tmp/clean_cfg.txt /root/hwconfig/config622.txt",
    "sync",
    "mount / -oro,remount",
    "killall ir"
]

print("Applying configuration and restarting ir...")
ok, out = send_telnet_commands(cmds)
print("Telnet output:", out)

print("Waiting 6 seconds for ir to restart...")
time.sleep(6)

ok, ps_out = send_telnet_commands([
    "ps | grep ir",
    "tail -n 25 /tmp/POKD_Log.txt"
])
print("=== IR STATUS ===")
print(ps_out)
