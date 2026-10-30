with open("ir_bin", "rb") as f:
    content = f.read()

# Let's find where "vSkipPresetNextPrevious" is in .dynsym or code
# In extract_syms earlier:
# Let's search for the function that uses the string "vSkipPresetNextPrevious"
pos = content.find(b"vSkipPresetNextPrevious\x00")
print(f"String 'vSkipPresetNextPrevious' at 0x{pos:x}")

# Let's search for references to this string or functions in preset_handler.c
for off in range(0, 0x16b000, 4):
    val = int.from_bytes(content[off:off+4], "little")
    if val == (pos + 0x8000):
        print(f"Ref at 0x{off:x}")
