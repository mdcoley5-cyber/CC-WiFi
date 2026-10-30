with open("ir_bin", "rb") as f:
    content = f.read()

# Search for 0x207 in literal pools
for idx in range(0, 0x16b000, 4):
    if int.from_bytes(content[idx:idx+4], "little") == 0x207:
        print(f"0x207 at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
