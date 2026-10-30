with open("ir_bin", "rb") as f:
    content = f.read()

target = 0x139cac
for i in range(0x16b000, 0x175000, 4):
    if int.from_bytes(content[i:i+4], "little") == target:
        print(f"Data entry at 0x{i:x}")
        # print entry
        for j in range(i-4, i+32, 4):
            v = int.from_bytes(content[j:j+4], "little")
            print(f"  0x{j:x}: 0x{v:08x}")
