import socket

ip = "192.168.1.123"
for port in range(1, 1024):
    try:
        s = socket.socket()
        s.settimeout(0.05)
        res = s.connect_ex((ip, port))
        s.close()
        if res == 0:
            print(f"Port {port} is OPEN on {ip}!")
    except Exception:
        pass
print("Scan done.")
