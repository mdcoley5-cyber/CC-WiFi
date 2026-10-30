import re

with open("ir_bin", "rb") as f:
    content = f.read()

for m in re.finditer(b"udhcpc[^\x00]*", content):
    print(m.group(0))

for m in re.finditer(b"ifconfig[^\x00]*", content):
    print(m.group(0))
