import struct

with open("ir_bin", "rb") as f:
    content = f.read()

def search_addr(addr):
    needle = struct.pack("<I", addr)
    pos = 0
    found = []
    while True:
        idx = content.find(needle, pos)
        if idx == -1:
            break
        found.append(idx)
        pos = idx + 1
    return found

# 1254480 is "preset-selector" -> 0x13a450
print("References to 'preset-selector' (0x13a450):", [hex(x) for x in search_addr(0x13a450)])

# 1242912 is "presets-as-menu-items" -> 0x12f720 + 0x8000 = 0x137720
print("References to 'presets-as-menu-items' (0x137720):", [hex(x) for x in search_addr(0x137720)])

# "DSC_CONFIG_PRESET_SELECTOR"
# "DSC_CONFIG_PRESETS_AS_MENU_ITEMS"
for name in ["DSC_CONFIG_PRESET_SELECTOR", "DSC_CONFIG_PRESETS_AS_MENU_ITEMS", "PRS_PresetSelector"]:
    idx = content.find(name.encode("ascii"))
    if idx != -1:
        vaddr = idx + 0x8000
        refs = search_addr(vaddr)
        print(f"'{name}' at 0x{idx:x} (vaddr 0x{vaddr:x}), refs: {[hex(r) for r in refs]}")
