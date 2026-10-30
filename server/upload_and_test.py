import socket
import threading
import time
from app import send_telnet_commands, get_local_ip

def send_file_to_radio(local_path, remote_path):
    local_ip = get_local_ip()
    port = 9996
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("0.0.0.0", port))
    server_sock.listen(1)

    with open(local_path, "rb") as f:
        file_bytes = f.read()

    def trigger():
        time.sleep(0.3)
        send_telnet_commands([f"nc {local_ip} {port} > {remote_path}"])

    t = threading.Thread(target=trigger)
    t.start()
    conn, addr = server_sock.accept()
    conn.sendall(file_bytes)
    conn.close()
    server_sock.close()
    t.join()
    print(f"Sent {local_path} -> {remote_path} ({len(file_bytes)} bytes)")

print("Step 1: Uploading updated_menu.xml to /tmp/updated_menu.xml...")
send_file_to_radio("updated_menu.xml", "/tmp/updated_menu.xml")

print("Step 2: Uploading updated_config622.txt to /tmp/updated_config622.txt...")
send_file_to_radio("updated_config622.txt", "/tmp/updated_config622.txt")

print("Step 3: Copying files to destination and restarting ir...")
cmds = [
    "cp /tmp/updated_menu.xml /mnt/config/SLR_TopLevelMenuCache.xml",
    "mount / -orw,remount",
    "cp /tmp/updated_config622.txt /root/hwconfig/config622.txt",
    "mount / -oro,remount",
    "killall ir"
]

ok, out = send_telnet_commands(cmds)
print(out)

print("Waiting 5 seconds for ir to restart...")
time.sleep(5)

ok, ps_out = send_telnet_commands(["ps | grep ir", "cat /tmp/POKD_Log.txt | grep -i preset"])
print("Process and POKD check:")
print(ps_out)
