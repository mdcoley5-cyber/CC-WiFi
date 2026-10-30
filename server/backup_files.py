from app import send_telnet_commands

commands = [
    "cat /root/hwconfig/config622.txt",
    "cat /mnt/config/SLR_TopLevelMenuCache.xml"
]

ok, out = send_telnet_commands(commands)
parts = out.split("\n# ")

with open("backup_config622.txt", "w") as f:
    f.write(parts[0].replace("cat /root/hwconfig/config622.txt\r\n", ""))

if len(parts) > 1:
    with open("backup_SLR_TopLevelMenuCache.xml", "w") as f:
        f.write(parts[1].replace("cat /mnt/config/SLR_TopLevelMenuCache.xml\r\n", ""))

print("Backups saved successfully.")
