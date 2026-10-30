import re

with open("ir_bin", "rb") as f:
    content = f.read()

for pos in [83239, 1333236, 1373750, 1594820]:
    chunk = content[max(0, pos-150):min(len(content), pos+250)]
    clean = re.sub(r"\n+", "\n", "".join(chr(b) if 32 <= b <= 126 else "\n" for b in chunk))
    print(f"=== Offset {pos} ===")
    print(clean)
