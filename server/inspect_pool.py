with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect literal pool around 0x25b00
for i in range(0x25af0, 0x25b40, 4):
    val = int.from_bytes(content[i:i+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        off = val - 0x8000
        end = content.find(b"\0", off)
        if 0 < end - off < 60:
            s = content[off:end]
            str_val = f" -> '{s.decode('ascii', errors='ignore')}'"
    print(f"0x{i:x}: 0x{val:08x}{str_val}")
