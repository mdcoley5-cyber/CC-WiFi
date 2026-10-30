with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search where "MP:" or "IROD:" or "ATUN:" is parsed
for term in [b"MP:", b"IROD:", b"ATUN:"]:
    pos = content.find(term)
    print(f"{term} at 0x{pos:x}")
    # let's see surrounding strings
    chunk = content[max(0, pos-100):pos+200]
    for s in chunk.split(b"\x00"):
        if s:
            print("  ", s)
