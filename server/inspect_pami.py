import struct

with open("ir_bin", "rb") as f:
    content = f.read()

chunk = content[0x16e91c - 4 : 0x16e91c + 32]
print("Table entry around 0x16e91c (presets-as-menu-items):")
for i in range(0, len(chunk), 4):
    val = struct.unpack("<I", chunk[i:i+4])[0]
    print(f"  +0x{i-4:x}: 0x{val:08x}")
