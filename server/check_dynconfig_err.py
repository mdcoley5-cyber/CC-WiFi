import re

with open("ir_bin", "rb") as f:
    content = f.read()

pos = content.find(b"dynconfig.c\x00")
print(f"dynconfig.c string at 0x{pos:x}")

chunk = content[0x128f00:0x129600]
for s in chunk.split(b"\x00"):
    if len(s) > 3 and all(32 <= b <= 126 for b in s):
        print("  RO:", s.decode('ascii'))
