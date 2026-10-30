with open("ir_bin", "rb") as f:
    content = f.read()

pos = content.find(b"vDisplayPresetMenu")
print(f"vDisplayPresetMenu at 0x{pos:x}")
if pos != -1:
    vaddr = pos + 0x8000
    for i in range(0, 0x16b000, 4):
        if int.from_bytes(content[i:i+4], "little") == vaddr:
            print(f"Ref at 0x{i:x}")
