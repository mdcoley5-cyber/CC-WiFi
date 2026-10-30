import re

with open("e:/Antigravity/CC WiFi/backup/mtd0_NAND_BootAgent.bin", "rb") as f:
    data = f.read()

print(f"BootAgent size: {len(data)} bytes")
# Extract printable strings
strings = re.findall(b"[\x20-\x7e]{3,}", data)
for s in strings:
    print(s.decode('ascii'))
