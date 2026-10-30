from app import send_telnet_commands

commands = [
    "cat /mnt/config/SLR_TopLevelMenuCache.xml"
]

ok, out = send_telnet_commands(commands)
with open("menu_cache.xml", "w") as f:
    f.write(out)

print(f"Saved menu_cache.xml: {len(out)} chars")
