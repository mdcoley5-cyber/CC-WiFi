with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect literal pool and code around 0x34ecc to 0x34f60
for i in range(0x34ee0, 0x34f60, 4):
    val = int.from_bytes(content[i:i+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        off = val - 0x8000
        end = content.find(b"\0", off)
        if 0 < end - off < 100:
            str_val = f" -> {content[off:end]}"
    print(f"0x{i:x}: 0x{val:08x}{str_val}")
