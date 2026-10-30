from app import send_telnet_commands

commands = [
    "cat /tmp/POKD_Log.txt | tail -n 30"
]

ok, out = send_telnet_commands(commands)
print(out)
