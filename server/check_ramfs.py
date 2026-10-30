from app import send_telnet_commands

commands = [
    "ls -la /mnt/ramfs/tmp",
    "ls -la /mnt/ramfs/tmp/config*"
]

ok, out = send_telnet_commands(commands)
print(out)
