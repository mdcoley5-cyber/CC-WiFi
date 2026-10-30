with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search for comparisons or case statements with 0x177 (NEXT_PRESET) and 0x178 (PREVIOUS_PRESET)
# In ARM, cmp rX, #0x177 -> 0x177 cannot be 8-bit rotated immediate!
# So it will be loaded from literal pool: 0x00000177 and 0x00000178
for idx in range(0, 0x16b000, 4):
    val = int.from_bytes(content[idx:idx+4], "little")
    if val == 0x177:
        print(f"0x177 at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
    elif val == 0x178:
        print(f"0x178 at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
    elif val == 0x153:
        print(f"0x153 (PRESET_MENU) at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
