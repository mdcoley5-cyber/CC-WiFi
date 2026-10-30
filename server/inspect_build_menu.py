import re

with open("ir_bin", "rb") as f:
    content = f.read()

# 0x0003c460 is vaddr -> file offset 0x0003c460 - 0x8000 = 0x34460
off = 0x34460
chunk = content[off:off+2000]

# Let's find all string references in this chunk
for i in range(0, len(chunk), 4):
    val = int.from_bytes(chunk[i:i+4], "little")
    if 0x8000 <= val < 0x16b000:
        s_off = val - 0x8000
        end = content.find(b"\0", s_off)
        if 0 < end - s_off < 100:
            s = content[s_off:end]
            if all(32 <= b <= 126 or b in [10, 13] for b in s):
                print(f"  +0x{i:03x} (0x{off+i:x}): {s.decode('ascii', errors='ignore')}")
