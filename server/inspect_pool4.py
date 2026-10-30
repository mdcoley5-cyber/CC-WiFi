with open("ir_bin", "rb") as f:
    content = f.read()

# literal pool at 0x23e78 + 0x3c + 8 + 0xa4 = 0x23f60
for i in range(0x23f40, 0x23f80, 4):
    val = int.from_bytes(content[i:i+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        s_off = val - 0x8000
        end = content.find(b"\0", s_off)
        if 0 < end - s_off < 60:
            str_val = f" -> {content[s_off:end]}"
    print(f"0x{i:x}: 0x{val:08x}{str_val}")
