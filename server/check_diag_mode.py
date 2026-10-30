with open("e:/Antigravity/CC WiFi/backup/mtd0_NAND_BootAgent.bin", "rb") as f:
    data = f.read()

pos = data.find(b"Diagnostic Test Mode")
print(f"Diagnostic Test Mode at 0x{pos:x}")

# Let's search references to this string in BootAgent
target = pos # offset in BootAgent (base is usually 0 or 0x30000000)
# BootAgent runs at address 0x0 or 0x30000000
for i in range(0, len(data), 4):
    val = int.from_bytes(data[i:i+4], "little")
    if (val & 0xffff) == (pos & 0xffff):
        print(f"Ref at 0x{i:x}: 0x{val:08x}")
