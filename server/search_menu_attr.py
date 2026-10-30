import re

with open("ir_bin", "rb") as f:
    content = f.read()

for m in re.finditer(b"menu=\"([^\"]+)\"", content):
    print(f"menu attr: {m.group(0)}")

for m in re.finditer(b"menu=", content):
    pos = m.start()
    chunk = content[pos-20:pos+50]
    print(f"menu= at 0x{pos:x}: {chunk}")
