import re

with open("ir_bin", "rb") as f:
    content = f.read()

# Extract all ASCII strings >= 4 chars
strings = re.findall(b"[\x20-\x7e]{4,}", content)
str_list = [s.decode("ascii", errors="ignore") for s in strings]

print(f"Total strings: {len(str_list)}")

print("\n--- Strings containing 'presets-as-menu-items' ---")
for s in str_list:
    if "presets-as-menu" in s.lower():
        print(s)

print("\n--- Strings containing 'PRESET' ---")
preset_strs = set(s for s in str_list if "preset" in s.lower())
for s in sorted(preset_strs):
    if len(s) < 40:
        print(s)

print("\n--- Strings containing 'client-menu' or 'item-group' or 'TopLevelMenu' ---")
for s in str_list:
    if any(k in s for k in ["client-menu", "item-group", "TopLevelMenu", "STATIONS_ITEMS", "my-stuff"]):
        print(s)
