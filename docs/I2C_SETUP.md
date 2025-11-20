# I2C Setup Guide for Raspberry Pi LCD Display

Complete guide for enabling and configuring I2C interface on Raspberry Pi to work with LCD displays.

---

## 📖 What is I2C?

**I2C** (Inter-Integrated Circuit) is a communication protocol that allows the Raspberry Pi to communicate with external devices like LCD displays. It uses only 2 data lines (SDA and SCL) plus power, making it much simpler than traditional parallel connections.

**Benefits of I2C LCD:**
- ✅ Only 4 wires needed (GND, VCC, SDA, SCL) instead of 16+
- ✅ Simple connection and cleaner wiring
- ✅ Multiple I2C devices can share the same bus
- ✅ Less GPIO pins used

---

## ⚠️ Critical Information

> **The I2C interface is DISABLED by default on Raspberry Pi.**  
> You **must** enable it before any I2C device (including LCD displays) will work!

**Without enabling I2C:**
- The Raspberry Pi cannot detect the LCD module
- Commands like `i2cdetect` will show empty results
- Your Python scripts will fail with I2C errors
- The display will remain blank even if powered correctly

---

## 🔧 Step-by-Step I2C Setup

### Step 1: Enable I2C Interface

**Open Raspberry Pi Configuration:**

```bash
sudo raspi-config
```

**Navigate through the menus:**
1. Select: **Interfacing Options** (or **Interface Options** on newer versions)
2. Select: **I2C**
3. Select: **Yes** to enable the I2C interface
4. Select: **OK** to confirm
5. Select: **Finish** to exit

**Reboot your Raspberry Pi:**

```bash
sudo reboot
```

**Why reboot is necessary:**  
The system needs to reload kernel modules and device drivers for I2C to become active.

---

### Step 2: Verify I2C is Enabled

After reboot, check if I2C device is available:

```bash
ls /dev/i2c*
```

**Expected output:**
```
/dev/i2c-1
```

If you see `/dev/i2c-1`, I2C is successfully enabled! ✅

**Troubleshooting:**
- If nothing appears, I2C wasn't enabled properly - repeat Step 1
- Older Raspberry Pi models may show `/dev/i2c-0` instead

---

### Step 3: Install I2C Tools and Libraries

**Install required packages:**

```bash
sudo apt-get update
sudo apt-get install -y i2c-tools python3-smbus
```

**What each library does:**

| Package | Purpose | Why It's Needed |
|---------|---------|-----------------|
| **i2c-tools** | Command-line utilities for I2C | Provides `i2cdetect`, `i2cget`, `i2cset` commands to detect and interact with I2C devices |
| **python3-smbus** | Python library for I2C | Enables Python scripts to communicate with I2C devices using SMBus protocol |

**Without these libraries:**
- You cannot scan for I2C devices
- Python scripts cannot communicate with the LCD
- The project **will not work**

---

### Step 4: Detect Your LCD I2C Address

**Connect your LCD display** to the Raspberry Pi (see [README Hardware Setup](../README.md#-hardware-setup) for wiring).

**Scan for I2C devices:**

```bash
i2cdetect -y 1
```

**Example output:**

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --
```

**Understanding the output:**
- `--` means no device at that address
- `27` (or any hex number) means a device was detected
- `UU` means a kernel driver is using that address (this is normal)

**Common I2C LCD addresses:**
- `0x27` (most common)
- `0x3F` (some manufacturers)

---

### Step 5: Configure Your LCD Address

**Edit the project configuration file:**

```bash
nano /path_to_folder/rasp-crypto-ticker/config.py
```

**Update the LCD_CONFIG section:**

```python
LCD_CONFIG = {
    'address': 0x27,  # ← Change to YOUR detected address (0x27 or 0x3F)
    'port': 1,        # I2C bus (1 for Raspberry Pi 2/3/4, 0 for Pi 1)
    'max_size': 16    # LCD width (16 for 16x2 displays)
}
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

---

### Step 6: Test I2C Communication

**Test reading from the I2C device:**

```bash
i2cget -y 1 0x27
```

Replace `0x27` with your detected address.

**Expected result:**
- You should see a hexadecimal value (e.g., `0x08`)
- This means communication is working! ✅

**If you see an error:**
```
Error: Read failed
```
- Check your wiring connections
- Verify the LCD has power (backlight should be on)
- Try the other common address (0x3F if you tried 0x27)

---

## 🔍 Advanced I2C Commands

### Check I2C Bus Information

```bash
i2cdetect -l
```

Shows all available I2C buses.

### Read Byte from I2C Device

```bash
i2cget -y 1 0x27 0x00
```

Reads from register `0x00` at address `0x27`.

### Write Byte to I2C Device

```bash
i2cset -y 1 0x27 0x00 0xFF
```

Writes `0xFF` to register `0x00` at address `0x27`.

**⚠️ Warning:** Be careful with `i2cset` - writing wrong values can damage devices!

---

## 🐛 Troubleshooting

### No I2C Device Detected

**Symptom:** `i2cdetect -y 1` shows all `--` (no devices)

**Solutions:**
1. ✅ **Verify I2C is enabled:**
   ```bash
   ls /dev/i2c*
   ```
   Should show `/dev/i2c-1`. If not, re-enable I2C in raspi-config.

2. ✅ **Check wiring:**
   - GND → Pin 6 (Ground)
   - VCC → Pin 2 (5V)
   - SDA → Pin 3 (GPIO 2)
   - SCL → Pin 5 (GPIO 3)

3. ✅ **Check LCD power:**
   - Backlight should be ON
   - If backlight is off, VCC or GND connection is wrong

4. ✅ **Test with another I2C device:**
   - If available, test with a different I2C module to rule out LCD defect

5. ✅ **Check Raspberry Pi model:**
   - Some older Pi models use I2C bus 0 instead of 1
   - Try: `i2cdetect -y 0`

---

### LCD Backlight On But No Text

**Symptom:** LCD backlight is on, but no text appears

**Solutions:**
1. ✅ **Check I2C address in config:**
   - Ensure `config.py` has the correct address from `i2cdetect`

2. ✅ **Adjust contrast:**
   - Turn the small potentiometer on the back of the I2C module
   - Sometimes text is there but invisible due to low contrast

3. ✅ **Verify SDA/SCL connections:**
   - Power (VCC/GND) might be connected, but data lines might be loose
   - Swap SDA and SCL if you're not sure which is which

4. ✅ **Check RPLCD installation:**
   ```bash
   pip list | grep RPLCD
   ```
   Should show `RPLCD` with version number

---

### "UU" Appears Instead of Address

**Symptom:** `i2cdetect` shows `UU` at your device address

**This is NORMAL! ✅**

`UU` means a kernel driver has already claimed that I2C address. This happens when:
- A device driver is loaded and using the device
- Your application is running and controlling the LCD

**You can still use the device** - this is not an error!

---

### Permission Denied Errors

**Symptom:** 
```
Error: Could not open file '/dev/i2c-1': Permission denied
```

**Solution:**

Add your user to the `i2c` group:

```bash
sudo usermod -a -G i2c $USER
```

Then log out and log back in (or reboot).

**Verify group membership:**
```bash
groups
```

Should show `i2c` in the list.

---

### I2C Address Changed After Reboot

**Symptom:** LCD was working, but after reboot the address changed

**This is unusual** - I2C addresses are hardcoded on the module.

**Possible causes:**
1. You may have multiple I2C devices connected
2. The module might be defective
3. You may be looking at a different device

**Solution:**
- Run `i2cdetect -y 1` again
- Update `config.py` with the correct address
- Consider labeling your I2C modules if you have multiple

---

### LCD Works But Shows Garbage Characters

**Symptom:** LCD displays random characters or blocks

**Solutions:**
1. ✅ **Wrong I2C address:**
   - Re-run `i2cdetect -y 1`
   - Update `config.py`

2. ✅ **Loose connections:**
   - Check all 4 wires are firmly connected
   - Try reseating the connections

3. ✅ **Power supply issue:**
   - Raspberry Pi might not have enough power
   - Use a 2.5A+ power supply
   - Disconnect other USB devices

4. ✅ **Software issue:**
   - Restart the application
   - Reboot the Raspberry Pi

---

## 📚 Understanding I2C Technical Details

### I2C Protocol Basics

**I2C uses 2 bidirectional lines:**
- **SDA** (Serial Data): Transfers data between devices
- **SCL** (Serial Clock): Synchronizes data transfer timing

**How it works:**
1. Master (Raspberry Pi) sends START condition
2. Master sends device address (e.g., 0x27)
3. Device acknowledges if address matches
4. Master sends/receives data
5. Master sends STOP condition

### I2C Addresses Explained

**7-bit addressing:**
- I2C uses 7-bit addresses (0x00 to 0x7F)
- Sometimes displayed as 8-bit with read/write bit

**Example:**
- 7-bit address: `0x27` = `0010 0111` binary
- This is what you see in `i2cdetect`

**PCF8574 Expander:**
- Most I2C LCD modules use PCF8574 chip
- Has 3 address pins (A0, A1, A2) that can be configured
- Base address: `0x20` or `0x38`
- Your module's address depends on how these pins are set

### I2C Bus Speed

**Default speed:** 100 kHz (Standard mode)

**Can be changed in `/boot/config.txt`:**

```
dtparam=i2c_arm_baudrate=400000
```

This sets it to 400 kHz (Fast mode).

**For this project:** Default speed is fine, no changes needed.

---

## 🔗 Related Documentation

- **Hardware Setup**: See [README - Hardware Setup](../README.md#-hardware-setup)
- **Configuration**: See [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)
- **Troubleshooting**: See [FAQ.md](FAQ.md)
- **Architecture & Modules**: See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md)

---

## 🌐 External Resources

- **I2C Protocol Specification**: https://www.nxp.com/docs/en/user-guide/UM10204.pdf
- **Raspberry Pi I2C Documentation**: https://www.raspberrypi.org/documentation/hardware/raspberrypi/
- **Arduino e Cia Tutorial** (Portuguese): https://arduinoecia.com.br/como-usar-display-lcd-i2c-raspberry-pi/
- **Adafruit I2C Guide**: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
- **PCF8574 Datasheet**: https://www.ti.com/lit/ds/symlink/pcf8574.pdf

---

## ✅ Quick Reference Checklist

Before running the project, verify:

- [ ] I2C is enabled in raspi-config
- [ ] `/dev/i2c-1` device exists
- [ ] `i2c-tools` and `python3-smbus` are installed
- [ ] LCD is connected to correct pins (GND, VCC, SDA, SCL)
- [ ] `i2cdetect -y 1` shows your LCD address
- [ ] `config.py` has the correct I2C address
- [ ] LCD backlight is on (powered correctly)
- [ ] RPLCD library is installed (`pip list | grep RPLCD`)

If all items are checked, you're ready to run the project! 🚀

---

**Back to main README**: [README.md](../README.md)

