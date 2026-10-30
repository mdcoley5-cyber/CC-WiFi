with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect 0xcf180 literal pool
val = int.from_bytes(content[0xcf180:0xcf184], "little")
print(f"Table pointer at 0xcf180: 0x{val:08x}")
# Table pointer is in Segment 3 (data/rodata)
# Let's see file offset
table_off = val - 0x8000 if val < 0x16b000 else 0x16b000 + (val - 0x17b000)
print(f"Table file offset: 0x{table_off:x}")

for i in range(24):
    entry_addr = table_off + i*8
    id_val = int.from_bytes(content[entry_addr : entry_addr+4], "little")
    str_ptr = int.from_bytes(content[entry_addr+4 : entry_addr+8], "little")
    str_off = str_ptr - 0x8000 if str_ptr < 0x16b000 else 0x16b000 + (str_ptr - 0x17b000)
    end = content.find(b"\0", str_off)
    name = content[str_off:end].decode("ascii", errors="ignore")
    print(f"  [{i}]: id={id_val}, name='{name}'")
