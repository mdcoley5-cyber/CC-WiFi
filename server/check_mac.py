import re

with open("e:/Antigravity/CC WiFi/backup/mtd3_Config.bin", "rb") as f:
    data = f.read()

# MAC address pattern (6 hex bytes or colon separated)
matches = re.findall(b"([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})", data)
print("MACs:", set(matches))

# Also search for "00:0e:" or "00:1" (Reciva MAC prefix: 00:0e:c6 or 00:0e:9b or 00:1c:...)
reciva_macs = re.findall(b"00:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}", data)
print("Reciva MACs:", set(reciva_macs))
