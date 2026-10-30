with open("e:/Antigravity/CC WiFi/backup/mtd0_NAND_BootAgent.bin", "rb") as f:
    data = f.read()

for i in range(0x120, 0x2c0, 4):
    w = int.from_bytes(data[i:i+4], "little")
    desc = f"0x{w:08x}"
    if (w >> 24) == 0xeb:
        imm24 = w & 0x00ffffff
        if imm24 & 0x800000:
            imm24 -= 0x1000000
        cur_vaddr = i
        dest = cur_vaddr + 8 + (imm24 << 2)
        desc += f"  BL 0x{dest:x}"
    elif (w >> 24) == 0xea:
        imm24 = w & 0x00ffffff
        if imm24 & 0x800000:
            imm24 -= 0x1000000
        cur_vaddr = i
        dest = cur_vaddr + 8 + (imm24 << 2)
        desc += f"  B 0x{dest:x}"
    print(f"0x{i:03x}: {desc}")
