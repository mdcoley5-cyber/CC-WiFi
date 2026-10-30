# Jumper Restore Guide - C.Crane CC WiFi (Reciva Barracuda)

## 1. Overview & Purpose
This guide details the procedure to recover a locked/non-booting **C.Crane CC WiFi Radio** (Reciva Barracuda module, motherboard **King Champion MX-200F v2.0**).

### Root Cause of Lockup
* The radio's configuration file `/root/hwconfig/config622.txt` was edited with `max-presets 40` alongside `presets-as-menu-items on`.
* The Reciva executable (`/root/ir`) has a hardcoded 48-byte BSS buffer at `0x001ca1c8` that can hold at most 12 preset pointers. Setting 40 presets caused a buffer overflow into critical event loop pointers (`0x001ca1f8`), resulting in an immediate segmentation fault during boot.
* Linux `init` attempted to respawn `/root/autostart` 10 times in 2 seconds, triggered the rate limiter (`respawning too fast: disabled for 5 minutes`), and left the unit in a dark, headless state where LCD, buttons, and network power remained uninitialized.

### Why the Jumper Trick Works
* The radio determines its model configuration (`HWCONFIG 622`) via an analog resistor divider connected to ADC pins on the 40-pin daughtercard socket (`J1`).
* **Only `config622.txt` was modified.** All other hardware config files on flash (e.g., `config620.txt`, `config805.txt`, `config_noarch.txt`) are pristine factory files.
* Temporarily bridging one of the ADC pins to Ground changes the detected Hardware ID (e.g. from `622` to `620`).
* As a result, the radio **does not load `config622.txt`**. It boots cleanly, powers on the Ethernet interface, brings up the physical network link, and starts Sharpfin's Telnet daemon on port 23.
* Once Telnet is available, our automated script logs in and restores the clean factory backup `/root/hwconfig/config622.txt.orig`.
* Removing the jumper returns the radio to its factory `622` identity on next boot.

---

## 2. Verified Socket Pinout & Measurements

### Multimeter Ground Verification (Completed)
On the **40-pin socket (`J1`)** on the main motherboard:
* **Top Row (Even Pins):** Pin 16 and **Pin 40** are Ground (GND).
* **Bottom Row (Odd Pins):** Pin 9, Pin 23, and **Pin 31** are Ground (GND).

### Socket J1 Orientation
Looking at the motherboard with the 40-pin socket at the bottom:
* Silkscreen marking at far left: **`40`** (top row) and **`39`** (bottom row).
* Silkscreen marking at far right: **`2`** (top row) and **`1`** (bottom row).

```text
               --- MOTHERBOARD INTERIOR (UP) ---

TOP ROW (Even):   [40] [38] [36] [34] [32] [30] [28] [26] ... [4] [2]
BOTTOM ROW (Odd): [39] [37] [35] [33] [31] [29] [27] [25] ... [3] [1]
                   ^                   ^    ^    ^
                 Hole 1              Hole Hole Hole
                (Far Left)             5    6    7

               --- BOARD EDGE (DOWN) ---
```

---

## 3. Step-by-Step Jumper Procedure

### Step 3.1: Locate Holes 5 and 6
On the **Bottom Row (Odd Pins)**, count holes starting from the **far left (Hole 1 / Pin 39)** towards the right:

| Hole # (From Left) | Pin Number | Function | Measurement |
| :---: | :---: | :--- | :--- |
| **Hole 1** | **Pin 39** | PWREN | Logic |
| **Hole 2** | **Pin 37** | nRSTOUT | Reset out |
| **Hole 3** | **Pin 35** | nRESET | CPU Reset |
| **Hole 4** | **Pin 33** | nLED_ON | LED control |
| **Hole 5** | **Pin 31** | **SYSTEM GROUND (GND)** | **0.00 V / Beep to chassis** |
| **Hole 6** | **Pin 29** | **AIN2 (HWCONFIG Channel 2)** | **Analog divider voltage** |
| **Hole 7** | **Pin 27** | **AIN1 (HWCONFIG Channel 1)** | **Analog divider voltage** |

### Step 3.2: Insert the Jumper Wire
1. Take a thin piece of wire (such as a single strand from a copper wire, a breadboard jumper wire pin, or a small U-bend from a staple/paperclip).
2. Insert one end into **Hole 5 (Pin 31, GND)**.
3. Insert the other end into **Hole 6 (Pin 29, AIN2)**.
   *(Note: Hole 5 and Hole 6 are directly adjacent holes in the same bottom row!)*
4. Alternatively, you can bridge **Hole 5 (Pin 31, GND)** to **Hole 7 (Pin 27, AIN1)** — either connection safely grounds an ADC channel and forces a non-622 Hardware ID.

### Step 3.3: Reseat the Barracuda Daughtercard
1. Align the three male header pin blocks on the bottom of the Barracuda daughtercard with the three female sockets on the motherboard:
   * The 40-pin header on the bottom.
   * The two 20-pin headers on the top left and top right.
2. Ensure the jumper wire ends remain securely inside holes 5 and 6 as the daughtercard pins enter the socket.
3. Gently and firmly press the module down until fully seated.

---

## 4. Network Setup & Recovery Execution

### Step 4.1: Network Connection
1. Plug a standard RJ-45 Ethernet cable into the radio's wired LAN port.
2. Connect the other end of the cable directly to your home router or unmanaged network switch.
3. Keep the radio's power cord **unplugged** for now.

### Step 4.2: Launch the Recovery Monitor
On your PC (connected to the same local network):
1. Navigate to the repository root directory.
2. Run:
   **`Start_Radio_Recovery.bat`** (Windows)
   *(Or run: `python server/recover_radio.py`)*
3. A command window will open with a green title:
   ```text
   ==================================================
   Reciva Radio Auto-Recovery Monitor
   Watching network for radio boot (LAN & Wi-Fi)...
   ==================================================
   Scanning cycle 1... (waiting for radio power-on)
   ```

### Step 4.3: Apply Power to the Radio
1. Plug the 9V DC power cord into the radio's power jack.
2. What will happen:
   * The LCD backlight will flicker and the board will power on.
   * Because AIN2 is grounded, the radio detects Hardware ID `620` instead of `622`.
   * It skips the corrupted `config622.txt` and boots into clean default firmware.
   * Within 10–15 seconds, `./ir` powers up the Ethernet PHY chip.
   * **The Ethernet switch port link LED will light up.**
   * The radio requests an IP address via DHCP and starts `telnetd` on port 23.

### Step 4.4: Automated Restoration
The running script (`recover_radio.py`) will automatically:
1. Detect port 23 open on the radio's IP.
2. Log into the radio with standard credentials `admin / admin`.
3. Remount the root filesystem read-write: `mount / -orw,remount`.
4. Overwrite `/root/hwconfig/config622.txt` with factory clean `/root/hwconfig/config622.txt.orig`.
5. Overwrite `/mnt/config/SLR_TopLevelMenuCache.xml` with factory clean `/mnt/config/SLR_TopLevelMenuCache.xml.orig`.
6. Flush changes to NAND flash: `sync`.
7. Remount read-only: `mount / -oro,remount`.
8. Print the confirmation banner:
   ```text
   =================================================================
   >>> RECOVERY SUCCESSFUL! RESTORE OUTPUT: <<<
   RECOVERY_COMPLETED_SUCCESSFULLY
   =================================================================
   ALL FACTORY ORIGINALS RESTORED AND FLASH SYNCED!
   ```

---

## 5. Post-Recovery Steps (Cleanup)
Once the script prints `RECOVERY SUCCESSFUL`:
1. **Unplug the power cord** from the radio.
2. Unseat the Barracuda daughtercard from the motherboard sockets.
3. **Remove the jumper wire** from Hole 5 / Hole 6.
4. Reseat the Barracuda daughtercard securely back into the sockets.
5. Plug the power cord back into the radio.
6. The radio will now boot using its restored factory `config622.txt`.
7. The LCD will light up, display the clock and standby text (`CC WiFi Radio`), and the power/station buttons will respond normally.

> [!TIP]
> **Permanent Hardware Bypass Mod (Recommended):**
> Instead of using a loose jumper wire that requires unseating the daughtercard, you can solder a miniature momentary push-button across Pin 31 (GND, Hole 5) and Pin 29 (AIN2, Hole 6). 
> When pressed during power-on, it grounds AIN2 to activate HW 620 recovery mode instantly without taking the radio apart. When released, the radio runs normally in HW 622.

---

## 6. Files & Scripts Reference

| File | Location | Purpose |
| :--- | :--- | :--- |
| **`Start_Radio_Recovery.bat`** | Repository root | One-click Windows launcher for recovery |
| **`recover_radio.py`** | `server/` | Automated Telnet detection & restore script |
| **`config622.txt.orig`** | Radio `/root/hwconfig/` | Factory pristine configuration (1295 bytes) |
| **`config622.txt`** | `server/` | Local backup copy of factory configuration |
| **`SLR_TopLevelMenuCache.xml.orig`**| Radio `/mnt/config/` | Factory pristine menu XML (6706 bytes) |
| **`j1_resistors.jpg`** | `server/` | Close-up reference photo of socket J1 |
| **`fcc_img_2_0.jpg`** | `server/` | Full motherboard socket layout photo |
