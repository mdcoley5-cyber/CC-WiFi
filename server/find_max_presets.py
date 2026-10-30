with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search where "max-presets" is handled
# DSC_MAX_PRESETS
pos = content.find(b"DSC_MAX_PRESETS")
print(f"DSC_MAX_PRESETS string at 0x{pos:x}")

# Find Option table entry for max-presets
pos_str = content.find(b"max-presets\x00")
print(f"max-presets string at 0x{pos_str:x} (vaddr 0x{pos_str+0x8000:x})")

target = pos_str + 0x8000
for i in range(0, 0x16b000, 4):
    if int.from_bytes(content[i:i+4], "little") == target:
        print(f"Ref at 0x{i:x}")
