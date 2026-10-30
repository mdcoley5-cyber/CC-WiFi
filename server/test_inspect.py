from app import send_telnet_commands

commands = [
    "cat /etc/passwd",
    "cat /etc/shadow 2>/dev/null"
]

ok, out = send_telnet_commands(commands)
print(out)
