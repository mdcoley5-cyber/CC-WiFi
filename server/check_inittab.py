from app import send_telnet_commands

commands = [
    "cat /etc/inittab"
]

ok, out = send_telnet_commands(commands)
print(out)
