import re

with open("ir_bin", "rb") as f:
    content = f.read()

def search_text(term):
    matches = [m.start() for m in re.finditer(re.escape(term.encode("ascii")), content)]
    print(f"'{term}': {len(matches)} occurrences at {matches}")

for t in ["NEXT_PRESET", "PREVIOUS_PRESET", "PRESET_MENU", "preset-selector", "presets-as-menu-items", "vSkipPresetNextPrevious", "PRS_PresetSelector", "PresetSelector", "client-menu menu=\"PRESETS\""]:
    search_text(t)
