# C.Crane CC WiFi Radio - Modernization & Unbricking Suite

[![Hardware](https://img.shields.io/badge/Hardware-C.Crane%20CC%20WiFi-blue.svg)](https://www.ccrane.com)
[![SoC](https://img.shields.io/badge/SoC-Samsung%20S3C2410%20(ARM920T)-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Reciva%20Barracuda%20(HW622)-green.svg)]()
[![License](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)]()

Complete open-source toolkit to revive, modernize, and de-cloud the **C.Crane CC WiFi Internet Radio** (King Champion MX-200F v2.0 mainboard / Reciva Barracuda module).

---

## The Problem: Why This Project Exists

In early 2021, Reciva's parent company decommissioned the global Reciva web portal (`radio.reciva.com`, `gateway.reciva.com`). While these radios feature fantastic RF engineering and audio amplifiers, the cloud shutdown left them severely impaired:

1. **Dead Menu Lockups:** Selecting **"Stations"**, **"Podcasts"**, **"My Stuff"**, **"My Stations"**, or **"My Streams"** sends HTTP requests to dead servers. The radio hangs indefinitely on a perpetual **"Loading..."** screen.
2. **Obsolete Button Assignments:** The physical `<<` and `>>` buttons were hardcoded to UPnP Media Player track skipping, leaving no quick way to surf saved station presets.
3. **Modern HTTPS/TLS Incompatibility:** The 2007 embedded Linux system does not support modern TLS 1.2/1.3 ciphers, preventing the radio from playing modern HTTPS streaming links directly.
4. **Soft-Brick Vulnerability:** Experimenting with Reciva options (such as setting `max-presets 40`) causes a fatal buffer overflow in the `/root/ir` binary, killing network and LCD initialization and leaving the radio unresponsive.

---

## Solutions Provided

* **Clean LCD Menus:** Pruned dead cloud aggregator XML links from `/mnt/config/SLR_TopLevelMenuCache.xml`. The radio menu is snappy and clean, displaying only functional features: **Presets**, **History**, **FM**, **Alarm Clock**, **Sleep Timer**, and **Configure**.
* **Physical Preset Stepping Buttons:**
  * **`>>` (Button 3):** Mapped to `NEXT_PRESET` (cycles to the next station).
  * **`<<` (Button 2):** Mapped to `PREVIOUS_PRESET` (cycles to the previous station).
  * **`Reply` Button:** Mapped to `PRESET_MENU` (opens the visual on-screen preset selector).
  * **Rotary Dial Press (`Select`):** Immediately plays the highlighted station.
* **Direct Top-Level Station List:** Enabled `Option: presets-as-menu-items on` so your saved presets appear directly on the main menu by name (strictly maintaining the safe default buffer of 10 presets).
* **Smart Local Stream Bridge & Transcoder (Python/Flask):** Runs on your local network, converting modern HTTPS streams into HTTP MP3/AAC streams that the radio plays smoothly. Includes a web dashboard to search 40,000+ stations via Radio-Browser.info and save them to radio presets with one click.
* **Hardware Safety Net (Permanent Push-Button Bypass Mod):** Complete reverse-engineering of the motherboard socket (`J1`). Soldering a miniature tactile push-button across Pin 31 (GND) and Pin 29 (AIN2) allows anyone to force Hardware ID `620` during boot. If a bad config is ever applied, holding the button recovers the radio to Telnet in 10 seconds without disassembly.
* **Automated Network Recovery Tools:** Multi-threaded Python monitor that detects the radio over the network and automatically restores factory-clean configurations.

---

## Hardware Overview & Specifications

| Component | Specification |
| :--- | :--- |
| **Radio Model** | C.Crane CC WiFi Internet Radio |
| **Mainboard** | King Champion MX-200F Common Main Board Ver 2.0 |
| **Processor Module** | Reciva Barracuda (Model 805) |
| **SoC** | Samsung S3C2410A (ARM920T @ 200 MHz) |
| **RAM / Flash** | 32 MB SDRAM / 16 MB NAND Flash |
| **Hardware ID** | HWCONFIG 622 (`config622.txt`) |
| **Operating System** | Embedded Linux 2.6.x (Sharpfin patched) |

> [!CAUTION]
> **Critical Reciva Buffer Warning:**
> In the `/root/ir` binary, the internal pointer table for `presets-as-menu-items` is a fixed 48-byte BSS buffer (holding at most 12 pointers). **Never set `max-presets` to a value higher than 10.** Setting values like `40` causes an immediate buffer overflow into event loop function pointers, soft-bricking the unit on boot.

---

## Quick Start Guide

### Prerequisites
1. **Root Telnet Access:** The radio must have the standard [Sharpfin patch](https://www.sharpfin.org) installed, giving root access via Telnet on port 23 (`admin / admin`).
2. **Network Connection:** Connect the radio to your local network via Wi-Fi or its built-in RJ-45 Ethernet port.
3. **PC / Server:** Python 3.8+ installed on a computer connected to the same LAN.

---

### Step 1: Deploy Clean Menus and Key Navigation

1. Clone this repository:
   ```bash
   git clone https://github.com/mdcoley5-cyber/CC-WiFi.git
   cd CC-WiFi
   ```
2. Configure your radio's LAN IP address in `server/config.json`:
   ```json
   {
     "radio_ip": "192.168.1.xxx",
     "radio_user": "admin",
     "radio_pass": "admin",
     "port": 5000
   }
   ```
3. Prepare and deploy the clean configuration:
   ```bash
   python server/prepare_clean_setup.py
   python server/deploy_clean_setup.py
   ```
4. The script will automatically:
   * Upload the streamlined `SLR_TopLevelMenuCache.xml` to `/mnt/config/`.
   * Update `/root/hwconfig/config622.txt` with the new key mappings and preset options.
   * Restart `./ir`. Your radio LCD will immediately display the new streamlined menu!

---

### Step 2: Run the Smart Radio Bridge Dashboard

To manage presets and stream modern stations:
1. Double-click `Run_Smart_Radio_Bridge.bat` (or run `python server/app.py`).
2. Your browser will open to `http://localhost:5000`.
3. Browse and assign stations across 3 specialized tabs:
   * **Live Radio Directory:** Search over 62,000 stations with smart dual-search (names & tags), 21 curated genre buttons, country origin filters, and sorting by popularity or bitrate.
   * **Podcasts:** Search and stream global podcasts directly.
   * **Custom Stream URL:** Paste any direct MP3, AAC, or HTTPS stream URL with live browser preview and 1-click assignment.
4. Presets 1–10 are starred (`★`) to indicate direct access on the physical radio buttons and LCD main menu.

---

## Hardware Bypass & Emergency Unbricking

If you ever apply an invalid config setting that prevents the radio from booting, you do not need to discard the unit.

See the complete guide in [**`Jumper Restore.md`**](Jumper%20Restore.md).

### The Concept
The radio identifies its model via an analog resistor divider connected to ADC pins on socket `J1`. Grounding ADC channel `AIN2` forces Hardware ID `620`, which causes the radio to bypass the corrupted `config622.txt` and boot into clean factory firmware with Ethernet and Telnet active.

### Permanent Button Mod (Recommended)
Instead of inserting temporary wires, solder a miniature momentary push-button across **Pin 31 (Ground)** and **Pin 29 (AIN2)** on motherboard socket `J1` (Row 1, Holes 5 & 6 from the left):

```text
               --- MOTHERBOARD INTERIOR (UP) ---

TOP ROW (Even):   [40] [38] [36] [34] [32] [30] [28] [26] ... [4] [2]
BOTTOM ROW (Odd): [39] [37] [35] [33] [31] [29] [27] [25] ... [3] [1]
                                        ^    ^
                                      Pin  Pin
                                       31   29
                                     (GND)(AIN2)
                                       |    |
                                      [BUTTON]
```

* **Normal Boot:** Power on normally with the button released. The radio boots into HW 622.
* **Emergency Rescue:** Hold the button down while plugging in the power cord. Launch `Start_Radio_Recovery.bat` on your PC. Within 10 seconds, the recovery script detects the radio, restores factory files, and syncs flash automatically.

---

## Repository Structure

```text
CC-WiFi/
├── .gitignore
├── LICENSE                       # Creative Commons CC0 1.0 Universal
├── README.md                     # This documentation
├── Jumper Restore.md             # Detailed hardware unbricking guide
├── Launch_Reciva_Server.bat      # Helper script for Reciva server
├── Open_Radio_Dashboard.bat      # Opens the web dashboard
├── Run_Smart_Radio_Bridge.bat    # Launches local Python proxy and web UI
├── Start_Radio_Recovery.bat      # One-click automated recovery launcher
├── backup/                       # Pristine factory MTD partition dumps
│   ├── mtd0_NAND_BootAgent.bin
│   ├── mtd1_Linux_Kernel.bin
│   ├── mtd3_Config.bin
│   └── mtd4_Debug.bin
└── server/                       # Core python scripts, web app, and configs
    ├── app.py                    # Flask stream proxy & preset management server
    ├── config.json               # Local network configuration
    ├── config622.txt             # Factory reference hardware config
    ├── clean_config622.txt       # Optimized config with preset navigation
    ├── clean_SLR_TopLevelMenuCache.xml # Cleaned top-level menu
    ├── prepare_clean_setup.py    # Generator script for clean configs
    ├── deploy_clean_setup.py     # Automated Telnet deployment script
    └── recover_radio.py          # Network listener & auto-restore script
```

---

## Security & Privacy Notice

* All tools in this suite operate strictly within your private Local Area Network (LAN).
* No cloud accounts, tokens, or external authentication are required.
* Configuration files in this repository use generic placeholder addresses (`192.168.1.xxx`) to ensure zero exposure of private network topology.

---

## License & Acknowledgements

* Distributed under the **CC0 1.0 Universal (Public Domain)** / **MIT License**.
* Grateful acknowledgment to the **Sharpfin Project** and the pioneering Reciva reverse-engineering community whose foundational work made saving these devices possible.
