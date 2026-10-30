import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# sClientMenuNames is at vaddr 0x0019ec14
# In Segment 3: offset 0x16b000, vaddr 0x17b000
# file offset = 0x16b000 + (0x19ec14 - 0x17b000) = 0x18ec14
client_menu_off = 0x16b000 + (0x0019ec14 - 0x17b000)

print(f"client_menu_off: 0x{client_menu_off:x}")
# Let's read table of strings
for i in range(40):
    val = struct.unpack("<I", content[client_menu_off + i*4 : client_menu_off + (i+1)*4])[0]
    if val == 0:
        break
    # val is vaddr of string
    if 0x8000 <= val < 0x16b000:
        str_off = val - 0x8000
        end = content.find(b"\0", str_off)
        print(f"  [{i}]: 0x{val:08x} -> {content[str_off:end].decode('ascii', errors='ignore')}")
    else:
        print(f"  [{i}]: 0x{val:08x} (outside text)")
