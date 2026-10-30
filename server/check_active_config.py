from app import send_telnet_commands

commands = [
    "grep -n -E 'presets|preset' /mnt/ramfs/tmp/config622.txt",
    "grep -n -E 'Keymap' /mnt/ramfs/tmp/config622.txt",
    "grep -n -E 'menu' /mnt/ramfs/tmp/config622.txt"
]

ok, out = send_telnet_commands(commands)
print(out)
