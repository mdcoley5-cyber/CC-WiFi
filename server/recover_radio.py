import socket
import time
import sys
import threading

found_flag = threading.Event()

# Ignore known non-radio devices (like printer at .48)
IGNORED_IPS = {"192.168.1.48", "192.168.1.1"}

def try_restore_on_ip(ip, timeout=1.5):
    if found_flag.is_set() or ip in IGNORED_IPS:
        return False, ""
    try:
        s = socket.create_connection((ip, 23), timeout=timeout)
        s.settimeout(timeout)
        
        def read_until(pattern, max_bytes=2048):
            buf = b""
            while pattern not in buf and len(buf) < max_bytes:
                chunk = s.recv(512)
                if not chunk:
                    break
                buf += chunk
            return buf.decode('ascii', errors='ignore')

        # Read banner - must contain login:
        banner = read_until(b"login:", max_bytes=1024)
        if "login:" not in banner:
            s.close()
            return False, ""

        print(f"\n[{ip}] Found Reciva login prompt! Logging in as admin...", flush=True)
        s.sendall(b"admin\n")
        read_until(b"Password:")
        s.sendall(b"admin\n")
        prompt = read_until(b"#")
        if "#" not in prompt:
            s.close()
            return False, ""

        print(f"[{ip}] Shell access granted (# prompt)! Restoring factory backups...", flush=True)

        cmds = [
            "mount / -orw,remount",
            "cp /root/hwconfig/config622.txt.orig /root/hwconfig/config622.txt",
            "cp /mnt/config/SLR_TopLevelMenuCache.xml.orig /mnt/config/SLR_TopLevelMenuCache.xml",
            "sync",
            "mount / -oro,remount",
            "cat /root/hwconfig/config622.txt | tail -n 8",
            "echo 'RECOVERY_COMPLETED_SUCCESSFULLY'"
        ]

        output = []
        for cmd in cmds:
            s.sendall(cmd.encode('ascii') + b"\n")
            res = read_until(b"#")
            output.append(res)

        s.sendall(b"exit\n")
        s.close()
        found_flag.set()
        return True, "\n".join(output)
    except Exception:
        return False, ""

def sweep_worker(ip_list):
    for ip in ip_list:
        if found_flag.is_set():
            return
        ok, res = try_restore_on_ip(ip, timeout=0.8)
        if ok:
            print("\n" + "="*65, flush=True)
            print(">>> RECOVERY SUCCESSFUL! RESTORE OUTPUT: <<<", flush=True)
            print(res, flush=True)
            print("="*65, flush=True)
            print("ALL FACTORY ORIGINALS RESTORED AND FLASH SYNCED!", flush=True)
            print("Next steps:", flush=True)
            print("  1. Unplug power cord from radio.")
            print("  2. Remove the jumper wire from the socket.")
            print("  3. Plug power back into radio.")
            print("  4. Radio will boot normally with factory CC WiFi settings!", flush=True)
            print("="*65, flush=True)
            return

def main():
    print("==================================================", flush=True)
    print("Reciva Radio Auto-Recovery Monitor")
    print("Watching network for radio boot (LAN & Wi-Fi)...", flush=True)
    print("==================================================", flush=True)
    
    # Priority IPs (original radio IP and fallback IPs)
    priority_ips = ["192.168.1.141", "192.168.1.180", "192.168.1.212"]
    
    iteration = 0
    while not found_flag.is_set():
        iteration += 1
        print(f"Scanning cycle {iteration}... (waiting for radio power-on)", flush=True)
        
        # Test priority candidate IPs first
        for ip in priority_ips:
            if found_flag.is_set():
                break
            ok, res = try_restore_on_ip(ip, timeout=1.0)
            if ok:
                print("\n" + "="*65, flush=True)
                print(">>> RECOVERY SUCCESSFUL! RESTORE OUTPUT: <<<", flush=True)
                print(res, flush=True)
                print("="*65, flush=True)
                print("ALL FACTORY ORIGINALS RESTORED AND FLASH SYNCED!", flush=True)
                print("Next steps:", flush=True)
                print("  1. Unplug power cord from radio.")
                print("  2. Remove the jumper wire from the socket.")
                print("  3. Plug power back into radio.")
                print("  4. Radio will boot normally with factory CC WiFi settings!", flush=True)
                print("="*65, flush=True)
                return

        # Parallel sweep across whole 192.168.1.x subnet in case DHCP gave a new IP
        all_ips = [f"192.168.1.{i}" for i in range(2, 255) if f"192.168.1.{i}" not in priority_ips and f"192.168.1.{i}" not in IGNORED_IPS]
        chunks = [all_ips[i:i+30] for i in range(0, len(all_ips), 30)]
        threads = [threading.Thread(target=sweep_worker, args=(c,)) for c in chunks]
        for t in threads: t.start()
        for t in threads: t.join()

        time.sleep(1.5)

if __name__ == "__main__":
    main()
