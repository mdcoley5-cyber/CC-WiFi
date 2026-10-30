import socket
import threading
import time
from app import send_telnet_commands, get_local_ip

def fetch_file(remote_path, local_path):
    local_ip = get_local_ip()
    port = 9998
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("0.0.0.0", port))
    server_sock.listen(1)

    def trigger():
        time.sleep(0.3)
        send_telnet_commands([f"nc {local_ip} {port} < {remote_path}"])

    t = threading.Thread(target=trigger)
    t.start()
    conn, addr = server_sock.accept()
    data = b""
    while True:
        chunk = conn.recv(16384)
        if not chunk:
            break
        data += chunk
    conn.close()
    server_sock.close()
    t.join()

    with open(local_path, "wb") as f:
        f.write(data)
    print(f"Downloaded {remote_path} to {local_path} ({len(data)} bytes)")

fetch_file("/root/hwconfig/config622.txt", "config622.txt")
fetch_file("/mnt/config/SLR_TopLevelMenuCache.xml", "SLR_TopLevelMenuCache.xml")
