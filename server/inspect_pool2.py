with open("ir_bin", "rb") as f:
    content = f.read()

# Let's inspect instructions and literal pool at 0x717d0 - 0x71950
for addr in range(0x717ec, 0x718c0, 12):
    # each registration is 3 instructions:
    # ldr r0, ...
    # ldr r1, ...
    # bl vMNR_RegisterClientMenu
    pass

# Let's just find all strings referenced in range 0x717a0..0x71980
print("=== Literal pool around 0x718d0 ===")
for i in range(0x718b8, 0x71980, 4):
    val = int.from_bytes(content[i:i+4], "little")
    str_val = ""
    if 0x8000 <= val < 0x16b000:
        off = val - 0x8000
        end = content.find(b"\0", off)
        if 0 < end - off < 60:
            s = content[off:end]
            str_val = f" -> '{s.decode('ascii', errors='ignore')}'"
    print(f"0x{i:x}: 0x{val:08x}{str_val}")
