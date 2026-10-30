import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# vMNR_RegisterClientMenu is at 0x000d71c4 (vaddr) -> offset 0x000d71c4 - 0x8000 = 0xcf1c4
# Let's find callers (bl instruction to 0x000d71c4)
# In ARM, BL instruction is 0xeb000000 | (offset & 0x00ffffff)
target_vaddr = 0x000d71c4

for idx in range(0, 0x16b000, 4):
    inst = struct.unpack("<I", content[idx:idx+4])[0]
    if (inst >> 24) == 0xeb: # BL
        # calculate target
        imm24 = inst & 0x00ffffff
        if imm24 & 0x800000:
            imm24 -= 0x1000000
        cur_vaddr = idx + 0x8000
        dest = cur_vaddr + 8 + (imm24 << 2)
        if dest == target_vaddr:
            print(f"Call to vMNR_RegisterClientMenu at 0x{idx:x} (vaddr 0x{cur_vaddr:x})")
