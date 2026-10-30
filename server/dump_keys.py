with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect the entire key string table from 0x128800 to 0x129000
for i in range(0x128a00, 0x128f00, 4):
    v = int.from_bytes(content[i:i+4], "little")
    if 0x8000 <= v < 0x16b000:
        s_off = v - 0x8000
        end = content.find(b"\0", s_off)
        if 0 < end - s_off < 40:
            s = content[s_off:end].decode('ascii', errors='ignore')
            if s.isupper() and "_" in s or s in ["POWER", "BACK", "SELECT", "REPLY", "PLAY", "STOP", "ENTER", "LEFT", "RIGHT", "UP", "DOWN", "UNUSED", "FORWARD"]:
                print(f"0x{i:x}: {s}")
