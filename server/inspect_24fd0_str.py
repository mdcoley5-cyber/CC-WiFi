with open("ir_bin", "rb") as f:
    content = f.read()

for addr in [0x24fd0 + 0x3c + 8 + 0xd4, 0x24fd0 + 0x44 + 8 + 0xd0]:
    val = int.from_bytes(content[addr:addr+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        s_off = val - 0x8000
        end = content.find(b"\0", s_off)
        str_val = f" -> {content[s_off:end]}"
    print(f"0x{addr:x}: 0x{val:08x}{str_val}")
