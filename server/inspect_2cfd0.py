with open("ir_bin", "rb") as f:
    content = f.read()

# 0x2cfd0 is vaddr -> file offset 0x24fd0
off = 0x24fd0
for i in range(off, off+80, 4):
    val = int.from_bytes(content[i:i+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        s_off = val - 0x8000
        end = content.find(b"\0", s_off)
        if 0 < end - s_off < 60:
            str_val = f" -> {content[s_off:end]}"
    print(f"0x{i:x}: 0x{val:08x}{str_val}")
