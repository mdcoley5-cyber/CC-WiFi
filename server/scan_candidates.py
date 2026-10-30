import socket

ips = ["192.168.1.41", "192.168.1.48", "192.168.1.64", "192.168.1.68", "192.168.1.90", "192.168.1.113", "192.168.1.124", "192.168.1.221", "192.168.1.141"]

for ip in ips:
    for port in (23, 80):
        try:
            s = socket.create_connection((ip, port), timeout=0.5)
            s.close()
            print(f"FOUND OPEN PORT {port} ON {ip}!")
        except Exception:
            pass
print("Scan done.")
