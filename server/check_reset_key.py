import re

with open("ir_bin", "rb") as f:
    content = f.read()

pos = content.find(b"power-on-reset-key")
print(f"power-on-reset-key at 0x{pos:x}")
chunk = content[pos-100:pos+200]
for s in chunk.split(b"\x00"):
    if s:
        print("  ", s)
