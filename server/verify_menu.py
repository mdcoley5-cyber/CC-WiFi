from app import send_telnet_commands

commands = [
    "head -n 60 /mnt/config/SLR_TopLevelMenuCache.xml | tail -n 15"
]

ok, out = send_telnet_commands(commands)
print(out)
