with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect the key event table around 0x128d80
# Each entry is (event_id, string_pointer) or similar
for i in range(0x128d00, 0x128e00, 8):
    val1 = int.from_bytes(content[i:i+4], "little")
    val2 = int.from_bytes(content[i+4:i+8], "little")
    str_val = ""
    for v in [val1, val2]:
        if 0x8000 <= v < 0x16b000:
            s_off = v - 0x8000
            end = content.find(b"\0", s_off)
            if 0 < end - s_off < 40:
                str_val = f"'{content[s_off:end].decode('ascii', errors='ignore')}'"
    print(f"0x{i:x}: 0x{val1:08x}, 0x{val2:08x} {str_val}")
