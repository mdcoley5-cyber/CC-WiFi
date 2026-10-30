import socket
import concurrent.futures

def check_ip(ip):
    for port in (23, 80):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            res = s.connect_ex((ip, port))
            s.close()
            if res == 0:
                return (ip, port)
        except Exception:
            pass
    return None

ips = [f"192.168.1.{i}" for i in range(1, 255)]
found = []

with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
    results = executor.map(check_ip, ips)
    for r in results:
        if r:
            found.append(r)

print("Scan results:", found)
