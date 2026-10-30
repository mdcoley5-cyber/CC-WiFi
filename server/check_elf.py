import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# Let's find pointers to 1254480 ("preset-selector")
str_offset = 1254480
# 32-bit little endian ARM
# Let's find where str_offset (as 0x... or relative) appears
# The ELF load address:
# Let's inspect ELF header
load_addr = 0x8000 # usually 0x8000 for ARM Linux
# Let's check ELF program headers
elf_magic = content[:4]
print("ELF magic:", elf_magic)
e_phoff = struct.unpack("<I", content[28:32])[0]
e_phnum = struct.unpack("<H", content[44:46])[0]
print(f"phoff={e_phoff}, phnum={e_phnum}")
for i in range(e_phnum):
    p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = struct.unpack("<IIIIIIII", content[e_phoff+i*32:e_phoff+(i+1)*32])
    print(f"Segment {i}: offset=0x{p_offset:x}, vaddr=0x{p_vaddr:x}, filesz=0x{p_filesz:x}")

