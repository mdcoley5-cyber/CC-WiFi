import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect around 0x17255c (which is in the data section: 0x16b000 - 0x1ba028)
# In Segment 3: offset 0x16b000, vaddr 0x17b000
# Notice that file offset 0x17255c corresponds to vaddr 0x17b000 + (0x17255c - 0x16b000) = 0x18255c
vaddr_preset_selector = 0x17b000 + (0x17255c - 0x16b000)
print(f"preset-selector entry at vaddr 0x{vaddr_preset_selector:x}")

# Let's see what references 0x18255c or what the table format is
# Let's dump 64 bytes around 0x17255c
chunk = content[0x17255c - 32 : 0x17255c + 64]
print("Table entry around 0x17255c:")
for i in range(0, len(chunk), 4):
    val = struct.unpack("<I", chunk[i:i+4])[0]
    print(f"  +0x{i-32:x}: 0x{val:08x}")
