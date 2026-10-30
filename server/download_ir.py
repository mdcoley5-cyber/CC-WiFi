import socket
import threading
import time
from app import send_telnet_commands, get_local_ip

local_ip = get_local_ip()
port = 9999

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(("0.0.0.0", port))
server_sock.listen(1)

def trigger_radio():
    time.sleep(0.5)
    send_telnet_commands([f"nc {local_ip} {port} < /root/ir"])

t = threading.Thread(target=trigger_radio)
t.start()

conn, addr = server_sock.accept()
data = b""
while True:
    chunk = conn.recv(65536)
    if not chunk:
        break
    data += chunk
conn.close()
server_sock.close()
t.join()

with open("ir_bin", "wb") as f:
    f.write(data)

print(f"Downloaded ir binary: {len(data)} bytes")
