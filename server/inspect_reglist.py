with open("ir_bin", "rb") as f:
    content = f.read()

# 0xd71a8 is vaddr -> file offset 0xcf1a8
off = 0xcf1a8
for i in range(off, off+60, 4):
    val = int.from_bytes(content[i:i+4], "little")
    print(f"0x{i:x}: 0x{val:08x}")
