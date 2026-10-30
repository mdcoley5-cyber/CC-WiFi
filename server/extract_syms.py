import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# dynsym at off 0x4918, size 0x9f50
# dynstr at off 0xe868, size 0xce98
dynsym_off = 0x4918
dynsym_size = 0x9f50
dynstr_off = 0xe868
dynstr_data = content[dynstr_off : dynstr_off + 0xce98]

num_syms = dynsym_size // 16
symbols = {}
for i in range(num_syms):
    st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack("<IIIBBH", content[dynsym_off + i*16 : dynsym_off + (i+1)*16])
    if st_name < len(dynstr_data):
        end = dynstr_data.find(b"\0", st_name)
        name = dynstr_data[st_name:end].decode("ascii", errors="ignore")
        if name:
            symbols[name] = st_value

for k in sorted(symbols.keys()):
    if any(x in k.lower() for x in ["preset", "menu", "key"]):
        print(f"{k:40s} = 0x{symbols[k]:08x}")
