import struct

with open("ir_bin", "rb") as f:
    content = f.read()

# Let's search symbol table if ELF has one
e_shoff = struct.unpack("<I", content[32:36])[0]
e_shentsize = struct.unpack("<H", content[46:48])[0]
e_shnum = struct.unpack("<H", content[48:50])[0]
e_shstrndx = struct.unpack("<H", content[50:52])[0]
print(f"shoff={e_shoff}, shentsize={e_shentsize}, shnum={e_shnum}")

# Read section headers
sections = []
for i in range(e_shnum):
    sec = struct.unpack("<IIIIIIIIII", content[e_shoff+i*40 : e_shoff+(i+1)*40])
    sections.append(sec)

if e_shstrndx < len(sections):
    shstr_sec = sections[e_shstrndx]
    shstr_data = content[shstr_sec[4] : shstr_sec[4]+shstr_sec[5]]
    def get_shname(off):
        end = shstr_data.find(b"\0", off)
        return shstr_data[off:end].decode("ascii", errors="ignore")

    for i, s in enumerate(sections):
        s_name = get_shname(s[0])
        print(f"Sec {i}: {s_name}, type=0x{s[1]:x}, addr=0x{s[3]:x}, off=0x{s[4]:x}, size=0x{s[5]:x}")
