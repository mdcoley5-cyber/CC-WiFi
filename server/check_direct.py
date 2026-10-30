import socket
import json

with open("config.json") as f:
    cfg = json.load(f)
radio_ip = cfg["radio_ip"]
print(f"Connecting to {radio_ip}...")

s = socket.create_connection((radio_ip, 23), timeout=5)
def read_until(pattern):
    buf = b""
    while pattern not in buf:
        chunk = s.recv(1024)
        if not chunk:
            break
        buf += chunk
    return buf.decode('ascii', errors='ignore')

read_until(b"login:")
s.sendall(b"admin\n")
read_until(b"Password:")
s.sendall(b"admin\n")
read_until(b"#")

def run(cmd):
    s.sendall(cmd.encode('ascii') + b"\n")
    return read_until(b"#")

print("config622.txt tail:")
print(run("tail -n 15 /tmp/config622.txt"))
print("POKD log check:")
print(run("grep -i presets-as-menu-items /tmp/POKD_Log.txt"))
print("ir running:")
print(run("ps | grep ir"))
s.sendall(b"exit\n")
s.close()
