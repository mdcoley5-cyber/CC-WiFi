with open("ir_bin", "rb") as f:
    content = f.read()

# NEXT_PRESET was at 1213496 (0x128438) -> vaddr 0x130438
# Let's search references to 0x130438
target = 0x130438
for idx in range(0, 0x16b000, 4):
    val = int.from_bytes(content[idx:idx+4], "little")
    if val == target:
        print(f"Ref to NEXT_PRESET at 0x{idx:x}")
