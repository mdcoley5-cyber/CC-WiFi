import re

with open("e:/Antigravity/CC WiFi/backup/mtd1_Linux_Kernel.bin", "rb") as f:
    data = f.read()

matches = re.findall(b"udhcpc[^\x00]*", data)
print("Matches in mtd1:", matches[:10])

matches_eth = re.findall(b"eth0[^\x00]*", data)
print("Matches eth0:", matches_eth[:10])
