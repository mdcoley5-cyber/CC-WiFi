import time
import socket
from app import send_telnet_commands, RADIO_IP

print("Sending reboot command to radio...")
send_telnet_commands(["reboot"])

print("Waiting for radio to go offline...")
time.sleep(3)

print("Waiting for radio to come back online...")
start_time = time.time()
while time.time() - start_time < 90:
    try:
        s = socket.create_connection((RADIO_IP, 23), timeout=1.5)
        s.close()
        print(f"Radio is BACK ONLINE after {int(time.time() - start_time)} seconds!")
        break
    except Exception:
        time.sleep(2)
else:
    print("Radio did not come back online within 90 seconds.")
