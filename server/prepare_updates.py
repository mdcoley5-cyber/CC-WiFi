import time
from app import send_telnet_commands

# 1. Prepare updated SLR_TopLevelMenuCache.xml
with open("SLR_TopLevelMenuCache.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

# Add <client-menu menu="PRESETS" icon="STATIONS">gettext:Presets</client-menu> right after <menu>
if '<client-menu menu="PRESETS" icon="STATIONS">gettext:Presets</client-menu>' not in xml_content:
    # Insert right at start of <menu>
    xml_content = xml_content.replace(
        '<menu><insert-item-group name="STATIONS_ITEMS"',
        '<menu><client-menu menu="PRESETS" icon="STATIONS">gettext:Presets</client-menu><insert-item-group name="STATIONS_ITEMS"'
    )

with open("updated_menu.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

# 2. Prepare updated config622.txt
with open("config622.txt", "r", encoding="utf-8") as f:
    cfg_content = f.read()

addition = """
Option:
presets-as-menu-items
on

Option:
max-presets
40
"""

if "presets-as-menu-items" not in cfg_content:
    cfg_content = cfg_content.strip() + "\n" + addition + "\n"

with open("updated_config622.txt", "w", encoding="utf-8") as f:
    f.write(cfg_content)

print("Files prepared successfully.")
