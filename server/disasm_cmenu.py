with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect instructions 0x34be0 to 0x34cb0
# and print what functions are called
for idx in range(0x34be0, 0x34cb0, 4):
    w = int.from_bytes(content[idx:idx+4], "little")
    desc = f"0x{w:08x}"
    if (w >> 24) == 0xeb:
        imm24 = w & 0x00ffffff
        if imm24 & 0x800000:
            imm24 -= 0x1000000
        cur_vaddr = idx + 0x8000
        dest = cur_vaddr + 8 + (imm24 << 2)
        desc += f"  BL 0x{dest:x}"
    elif (w & 0x0e5f0000) == 0x041f0000:
        u = (w >> 23) & 1
        imm = w & 0xfff
        pc = idx + 8
        dest = pc + imm if u else pc - imm
        val = int.from_bytes(content[dest:dest+4], "little")
        str_val = ""
        if 0x8000 <= val < 0x16b000:
            off = val - 0x8000
            end = content.find(b"\0", off)
            if 0 < end - off < 60:
                str_val = f" -> {content[off:end]}"
        desc += f"  LDR r{(w>>12)&0xf}, [0x{dest:x}] (=0x{val:08x}{str_val})"
    print(f"0x{idx:x}: {desc}")
