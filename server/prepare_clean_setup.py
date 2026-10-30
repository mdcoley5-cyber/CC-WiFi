import xml.etree.ElementTree as ET

# 1. Clean XML
clean_xml = """<top-level><config-predicates><config-predicate name="old-ui"><require option="ui-level" type="int" value="0"></require>
</config-predicate>
<config-predicate name="alarm-off"><require option="alarm-clock" type="select" value="off"></require>
</config-predicate>
<config-predicate name="sleep-in-main-menu"><require option="sleep-timer-in-main-menu" type="bool" value="true"></require>
</config-predicate>
</config-predicates>
<menu>
<client-menu menu="HISTORY" icon="STATIONS">gettext:History</client-menu>
<client-menu menu="FM" icon="FM">gettext:FM</client-menu>
<client-menu menu="ALARM" icon="ALARM" predicate="alarm-off" value="FALSE">gettext:Alarm Clock</client-menu>
<client-menu menu="SLEEP" icon="SLEEP">gettext:Sleep Timer</client-menu>
<client-menu menu="CONFIGURE" icon="CONFIGURE">gettext:Configure</client-menu>
</menu>
</top-level>
"""

# Validate XML
root = ET.fromstring(clean_xml)
print("XML is valid ElementTree! Tag:", root.tag)

with open("clean_SLR_TopLevelMenuCache.xml", "w", encoding="utf-8") as f:
    f.write(clean_xml)

# 2. Prepare new config622.txt
with open("config622.txt", "r", encoding="utf-8") as f:
    cfg = f.read()

lines = cfg.splitlines()
new_lines = []
for line in lines:
    if line.startswith("Keymap: r2c1"):
        new_lines.append("Keymap: r2c1 PREVIOUS_PRESET MP:SKIP_PREVIOUS IROD:SKIP_PREVIOUS ATUN:FM_STEP_DOWN")
    elif line.startswith("Keymap: r2c2"):
        new_lines.append("Keymap: r2c2 NEXT_PRESET MP:SKIP_NEXT IROD:SKIP_NEXT ATUN:FM_STEP_UP")
    else:
        new_lines.append(line)

new_lines.append("")
new_lines.append("# Button Reply opens Preset Menu")
new_lines.append("Keymap: r1c2 PRESET_MENU")
new_lines.append("")
new_lines.append("Option:")
new_lines.append("presets-as-menu-items")
new_lines.append("on")
new_lines.append("")

new_cfg = "\n".join(new_lines) + "\n"

with open("clean_config622.txt", "w", encoding="utf-8") as f:
    f.write(new_cfg)

print("clean_config622.txt prepared successfully. Total lines:", len(new_lines))
