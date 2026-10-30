with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect code around 0x258b4 and 0x25ae8
for addr in [0x25880, 0x25aa0]:
    chunk = content[addr:addr+100]
    # find any strings or references
    print(f"=== Offset 0x{addr:x} ===")
    for i in range(0, 80, 4):
        val = int.from_bytes(chunk[i:i+4], "little")
        # is it string pointer?
        str_val = ""
        if 0x8000 <= val < 0x16b000:
            off = val - 0x8000
            end = content.find(b"\0", off)
            if 0 < end - off < 60:
                s = content[off:end]
                if all(32 <= b <= 126 for b in s):
                    str_val = f" -> '{s.decode('ascii')}'"
        print(f"  +0x{i:02x}: 0x{val:08x}{str_val}")
