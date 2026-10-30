with open("ir_bin", "rb") as f:
    content = f.read()

target = 0x34f0c
for idx in range(0x34000, 0x35000, 4):
    w = int.from_bytes(content[idx:idx+4], "little")
    if (w & 0x0e5f0000) == 0x041f0000: # LDR Rd, [PC, +/-imm12]
        u = (w >> 23) & 1
        imm = w & 0xfff
        pc = idx + 8
        dest = pc + imm if u else pc - imm
        if dest == target:
            reg = (w >> 12) & 0xf
            print(f"LDR r{reg} at 0x{idx:x}")
