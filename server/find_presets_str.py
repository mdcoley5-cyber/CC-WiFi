with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search where "PRESETS" is used in stationr.c / client menu handling
pos = 0
while True:
    idx = content.find(b"PRESETS\x00", pos)
    if idx == -1:
        break
    print(f"Found 'PRESETS' at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
    pos = idx + 1
