import re

with open("ir_bin", "rb") as f:
    content = f.read()

def show_context(offset, size=300):
    chunk = content[offset:offset+size]
    # find any string pointers in this chunk
    # also print nearby debug strings
    print(f"=== Offset 0x{offset:x} ===")
    for m in re.finditer(b"[\x20-\x7e]{4,}", chunk):
        print(f"  String at +0x{m.start():x}: {m.group(0).decode('ascii', errors='ignore')}")

show_context(0x6c800, 400)
show_context(0x6d300, 400)
show_context(0x24600, 400)
