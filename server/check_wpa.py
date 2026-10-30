import re

with open("ir_bin", "rb") as f:
    content = f.read()

for m in re.finditer(b"wpa_supplicant[^\x00]*", content):
    print(m.group(0))
