from app import send_telnet_commands

commands = [
    "grep -n 'client-menu menu=\"PRESETS\"' /mnt/config/SLR_TopLevelMenuCache.xml"
]

ok, out = send_telnet_commands(commands)
print(out)
