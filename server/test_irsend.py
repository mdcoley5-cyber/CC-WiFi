from app import send_telnet_commands

commands = [
    "irsend SIMULATE '0000000000000000 00 p 00'",
    "irsend SIMULATE '0000000000000000 00 q 00'"
]

ok, out = send_telnet_commands(commands)
print(out)
