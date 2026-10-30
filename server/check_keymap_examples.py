from app import send_telnet_commands

commands = [
    "grep -h 'Keymap:' /root/hwconfig/*.txt | grep ':' | head -n 20"
]

ok, out = send_telnet_commands(commands)
print(out)
