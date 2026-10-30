from app import send_telnet_commands

commands = [
    "grep -rn 'RECIVA_HW_CONFIG' /etc /root",
    "grep -rn 'hwconfig' /etc /root"
]

ok, out = send_telnet_commands(commands)
print(out)
