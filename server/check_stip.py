import re

with open("e:/Antigravity/CC WiFi/backup/mtd3_Config.bin", "rb") as f:
    data = f.read()

for m in re.finditer(b"STIP[^\x00]*", data):
    chunk = data[m.start():m.start()+100]
    print(chunk[:50])

matches = re.findall(b"192\\.168\\.[0-9\\.]+", data)
print("IPs in mtd3_Config:", set(matches))
