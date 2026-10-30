import re

with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search for "MP:" or other prefixes in strings
matches = re.findall(b"[A-Z0-9_]+:", content)
# Filter reasonable prefix strings
valid = set()
for m in matches:
    s = m.decode('ascii', errors='ignore')
    if 2 <= len(s) <= 10 and s.isupper():
        valid.add(s)

print("Possible prefixes with colon:")
print(sorted(valid))

# Search where "Keymap:" is parsed
pos = content.find(b"Keymap:")
print(f"Keymap: at 0x{pos:x}")
# Let's find references to "Keymap:"
for i in range(0, 0x16b000, 4):
    if int.from_bytes(content[i:i+4], "little") == (pos + 0x8000):
        print(f"Ref at 0x{i:x}")
