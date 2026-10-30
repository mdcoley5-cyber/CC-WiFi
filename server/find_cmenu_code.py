with open("ir_bin", "rb") as f:
    content = f.read()

# 0x1342b4 is "Adding <client-menu menu=\"%s\"> as %s"
# Let's find where 0x1342b4 or near it is referenced in text section
# In ARM, adr/ldr pc relative or literal pool
for off in range(0, 0x120000, 4):
    w = int.from_bytes(content[off:off+4], "little")
    if abs(w - (0x1342b4 + 0x8000)) < 100:
        print(f"Match near 0x1342b4 at 0x{off:x}: 0x{w:08x}")
