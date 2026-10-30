import re

with open("e:/Antigravity/CC WiFi/backup/mtd3_Config.bin", "rb") as f:
    data = f.read()

# Let's search for fstab or mount points in mtd3_Config.bin
for m in re.finditer(b"/etc/fstab[^\x00]*", data):
    print(m.group(0))

for m in re.finditer(b"mtdblock[^\x00]*", data):
    print(m.group(0))
