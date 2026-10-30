with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect instructions calling 'Adding <client-menu' or 'Ignoring <client-menu'
# 0x34f0c is at vaddr 0x3cf0c
# Search references to 0x3cf0c or 0x3cf48
target = 0x0003cf0c
for idx in range(0x34000, 0x35000, 4):
    w = int.from_bytes(content[idx:idx+4], "little")
    if w == target:
        print(f"Literal pool entry at 0x{idx:x}")
    # or ldr pointing to 0x34f0c
    # ldr rx, [pc, #imm]
    if (w & 0xfffff000) == 0xe59f0000:
        offset = w & 0xfff
        pc = idx + 8
        if pc + offset == 0x34f0c:
            print(f"ldr at 0x{idx:x}")
