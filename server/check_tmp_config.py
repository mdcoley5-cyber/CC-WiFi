from app import send_telnet_commands

commands = [
    "ls -la /tmp",
    "cat /tmp/config* 2>/dev/null | head -n 30"
]

ok, out = send_telnet_commands(commands)
print(out)
