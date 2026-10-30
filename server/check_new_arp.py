import socket

new_ips = [
    "192.168.1.27", "192.168.1.121", "192.168.1.123", "192.168.1.153", 
    "192.168.1.202", "192.168.1.203", "192.168.1.211"
]

for ip in new_ips:
    for port in (23, 80, 21):
        try:
            s = socket.create_connection((ip, port), timeout=0.5)
            s.close()
            print(f"MATCH: {ip} port {port} is OPEN!")
        except Exception:
            pass

print("Scan complete.")
