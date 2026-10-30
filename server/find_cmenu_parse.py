import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# 0x1342b4 is at vaddr 0x1342b4 + 0x8000 = 0x13c2b4
vaddr = 0x13c2b4
# Let's find references
needle = struct.pack("<I", vaddr)
pos = 0
while True:
    idx = content.find(needle, pos)
    if idx == -1:
        break
    print(f"Ref to 'Adding <client-menu...': 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
    pos = idx + 1
