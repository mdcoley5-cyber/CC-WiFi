with open("ir_bin", "rb") as f:
    content = f.read()

# sClientMenuListNames = 0x0019ec0c
off = 0x16b000 + (0x0019ec0c - 0x17b000)
print(f"sClientMenuListNames offset: 0x{off:x}")
for i in range(16):
    addr = off + i*4
    val = int.from_bytes(content[addr:addr+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        s_off = val - 0x8000
        end = content.find(b"\0", s_off)
        str_val = f" -> '{content[s_off:end].decode('ascii', errors='ignore')}'"
    print(f"  [{i}]: 0x{val:08x}{str_val}")
