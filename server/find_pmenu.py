with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search around 0x128b00 - 0x128d00 for PRESET_MENU
pos = content.find(b"PRESET_MENU\x00")
print(f"PRESET_MENU string at 0x{pos:x} (vaddr 0x{pos+0x8000:x})")

target = pos + 0x8000
for i in range(0x128800, 0x129000, 4):
    if int.from_bytes(content[i:i+4], "little") == target:
        print(f"Table entry for PRESET_MENU at 0x{i:x}")
        # print 16 bytes around it
        for j in range(i-8, i+12, 4):
            v = int.from_bytes(content[j:j+4], "little")
            print(f"  0x{j:x}: 0x{v:08x}")
