import zlib

with open("e:/Antigravity/CC WiFi/backup/system_files_backup.tar.gz", "rb") as f:
    gz_data = f.read()

try:
    tar_data = zlib.decompress(gz_data, 16 + zlib.MAX_WBITS)
    print("Decompressed tar size:", len(tar_data))
    # search filenames in tar header
    for i in range(0, len(tar_data), 512):
        block = tar_data[i:i+512]
        name = block[:100].split(b"\x00")[0]
        if name:
            print("Tar entry:", name.decode('ascii', errors='ignore'))
except Exception as e:
    print("Decompress error:", e)
