from app import send_telnet_commands

commands = [
    "grep -n 'presets-as-menu-items' /tmp/POKD_Log.txt",
    "grep -n 'max-presets' /tmp/POKD_Log.txt",
    "cat /tmp/POKD_Log.txt | tail -n 25"
]

ok, out = send_telnet_commands(commands)
print(out)
