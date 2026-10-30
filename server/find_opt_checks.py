import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# In ARM assembly, loading a constant 0x75 or 0x257 or comparing:
# mov r1, #0x75 -> 0xe3a01075
# mov r0, #0x75 -> 0xe3a00075
# cmp rX, #0x75 -> ...
# Or ldr from literal pool: 0x00000075, 0x00000257

print("Literal 0x75 in text:")
for idx in range(0, 0x16b000, 4):
    val = struct.unpack("<I", content[idx:idx+4])[0]
    if val == 0x75:
        print(f"  at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
    elif val == 0x257:
        print(f"  0x257 at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")

print("Checking ARM instructions mov rx, #0x75:")
for idx in range(0, 0x16b000, 4):
    inst = struct.unpack("<I", content[idx:idx+4])[0]
    # mov rx, #0x75 is 0xe3a0x075
    if (inst & 0xfff0ffff) == 0xe3a00075:
        reg = (inst >> 12) & 0xf
        print(f"  mov r{reg}, #0x75 at 0x{idx:x} (vaddr 0x{idx+0x8000:x})")
    # mov rx, #0x257: 0x257 = (0x95 ror 30)? No, 0x257 cannot be encoded as 8-bit rotated immediate in ARM!
    # So 0x257 MUST be loaded from a literal pool or generated with 2 instructions!
