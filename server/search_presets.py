import re

with open("ir_bin", "rb") as f:
    content = f.read()

for m in re.finditer(b"PRESETS\x00", content):
    pos = m.start()
    chunk = content[max(0, pos-40):min(len(content), pos+60)]
    clean = re.sub(r"\n+", "\n", "".join(chr(b) if 32 <= b <= 126 else "\n" for b in chunk))
    print(f"=== MATCH 'PRESETS' at 0x{pos:x} ===")
    print(clean)
