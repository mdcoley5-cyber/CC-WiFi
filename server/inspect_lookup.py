with open("ir_bin", "rb") as f:
    content = f.read()

# 0xd7110 is vaddr -> file offset 0xcf110
off = 0xcf110
for idx in range(off, off+100, 4):
    w = int.from_bytes(content[idx:idx+4], "little")
    print(f"0x{idx:x}: 0x{w:08x}")
