from app import send_telnet_commands

commands = [
    "tail -n 20 /root/hwconfig/config622.txt"
]

ok, out = send_telnet_commands(commands)
print(out)
