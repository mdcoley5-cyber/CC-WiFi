import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# In extract_syms earlier:
# .bss is addr 0x1ca028, size 0x5950
# 0x001ca1c8 is in BSS (offset 0x1a0 bytes into BSS)
# Let's search references to 0x1ca1c8
target = 0x001ca1c8
for idx in range(0, 0x16b000, 4):
    if int.from_bytes(content[idx:idx+4], "little") == target:
        print(f"Ref to 0x1ca1c8 at 0x{idx:x}")

# Let's search what other variables are near 0x1ca1c8 (e.g. 0x1ca1c8 + 4*10 = 0x1ca1f0)
for idx in range(0, 0x16b000, 4):
    val = int.from_bytes(content[idx:idx+4], "little")
    if 0x001ca1c8 <= val <= 0x001ca270:
        print(f"Ref to 0x{val:08x} at 0x{idx:x}")
