from app import send_telnet_commands

cmds = [
    "mount / -orw,remount",
    "cp -p /root/hwconfig/config622.txt /root/hwconfig/config622.txt.orig",
    "cp -p /mnt/config/SLR_TopLevelMenuCache.xml /mnt/config/SLR_TopLevelMenuCache.xml.orig",
    "sync; mount / -oro,remount",
    "ls -l /root/hwconfig/config622.txt*",
    "ls -l /mnt/config/SLR_TopLevelMenuCache.xml*"
]

ok, out = send_telnet_commands(cmds)
print(out)
