import re

with open("ir_bin", "rb") as f:
    content = f.read()

def find_surroundings(pattern, length=500):
    for m in re.finditer(pattern, content):
        start = max(0, m.start() - 200)
        end = min(len(content), m.end() + 300)
        chunk = content[start:end]
        printable = "".join(chr(b) if 32 <= b <= 126 else "\n" for b in chunk)
        # deduplicate newlines
        clean = re.sub(r"\n+", "\n", printable)
        print(f"=== MATCH: {pattern} at {m.start()} ===")
        print(clean)

find_surroundings(b"vSkipPresetNextPrevious")
find_surroundings(b"NEXT_PRESET")
find_surroundings(b"PRESET_MENU")
find_surroundings(b"preset-selector")
find_surroundings(b"presets-as-menu-items")
