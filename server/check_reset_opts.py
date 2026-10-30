import re

with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search for boot keys or power on keys
for m in re.finditer(b"power-on[^\x00]*", content):
    print("Power-on opt:", m.group(0))

for m in re.finditer(b"factory-reset[^\x00]*", content):
    print("Factory reset:", m.group(0))
