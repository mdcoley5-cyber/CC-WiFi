import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# Let's find references to "vDisplayPresetMenu" or where presets-as-menu-items is used
# In find_opt_checks.py earlier:
# mov r0, #0x75 was at:
# 0x246a4 (vaddr 0x2c6a4)
# 0x25120 (vaddr 0x2d120)
# 0x25250 (vaddr 0x2d250)
# 0x2c68c (vaddr 0x3468c)
# 0x4b020 (vaddr 0x53020)
# 0xb8b44 (vaddr 0xc0b44)

for addr in [0x246a4, 0x25120, 0x25250, 0x2c68c, 0x4b020, 0xb8b44]:
    print(f"=== Check at 0x{addr:x} (vaddr 0x{addr+0x8000:x}) ===")
    chunk = content[addr-16:addr+64]
    for i in range(0, len(chunk), 4):
        w = int.from_bytes(chunk[i:i+4], "little")
        s = ""
        if (w >> 24) == 0xeb:
            imm24 = w & 0x00ffffff
            if imm24 & 0x800000:
                imm24 -= 0x1000000
            cur_vaddr = (addr - 16 + i) + 0x8000
            dest = cur_vaddr + 8 + (imm24 << 2)
            s = f"BL 0x{dest:x}"
        print(f"  +0x{i-16:02x}: 0x{w:08x} {s}")
