# Frequently Asked Questions (FAQ)

Common questions and answers about the Raspberry Pi Crypto Ticker.

---

## 🚀 Getting Started

### Which file should I run?

Run `python main.py` - this is the main application entry point.

```bash
cd /path_to_folder/rasp-crypto-ticker
python main.py
```

### Which configuration file should I edit?

Edit **`config.py`** - all settings are configured here. It's the single configuration file for the entire application.

See [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) for complete documentation.

### How do I start the application?

**Manually:**
```bash
cd /path_to_folder/rasp-crypto-ticker
python main.py
```

**As a service (automatically on boot):**
```bash
sudo systemctl start crypto_ticker.service
```

See [SYSTEMD_SETUP.md](SYSTEMD_SETUP.md) for service setup.

---

## ⚙️ Configuration

### How do I enable/disable modules?

Open `config.py` and set `enabled` to `True` or `False`:

```python
WEATHER_MODULE_CONFIG['enabled'] = False  # Disable weather & time
CRYPTO_MODULE_CONFIG['enabled'] = True    # Enable crypto
```

### Can I change the display order of modules?

Yes! Edit `MODULE_ORDER` in `config.py`:

```python
MODULE_ORDER = ['crypto', 'weather']  # Show crypto first
```

You can also repeat modules:
```python
MODULE_ORDER = ['crypto', 'crypto', 'weather']  # Crypto twice, then weather
```

### How do I change the display duration?

Edit the `display_duration` for each module in `config.py`:

```python
WEATHER_MODULE_CONFIG['display_duration'] = 15  # 15 seconds per screen
CRYPTO_MODULE_CONFIG['display_duration'] = 20   # 20 seconds per coin
```

### How do I change how often data updates?

Edit the `update_interval` (in seconds) in `config.py`:

```python
WEATHER_MODULE_CONFIG['update_interval'] = 300   # 5 minutes
CRYPTO_MODULE_CONFIG['update_interval'] = 900    # 15 minutes
```

**Note:** This affects API calls, not display rotation.

---

## 💰 Cryptocurrency

### Which crypto symbols should I use?

Use short acronyms (3-4 chars) mapped to CoinGecko IDs in `config.py`:

```python
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',      # Acronym: CoinGecko ID
    'ETH': 'ethereum',
    'SOL': 'solana',
}
```

**Why acronyms?** 16x2 LCD is small - short names fit better!

Find CoinGecko IDs: https://api.coingecko.com/api/v3/coins/list

### How do I add more cryptocurrencies?

Simply add to the `symbols` dictionary in `config.py`:

```python
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'ADA': 'cardano',       # Add these
    'DOT': 'polkadot',      # Add these
    'AVAX': 'avalanche-2',  # Add these
}
```

See [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) for 50+ cryptocurrency examples.

### Can I display prices in EUR/GBP instead of USD?

Yes! Change the `fiat` setting in `config.py`:

```python
CRYPTO_MODULE_CONFIG['fiat'] = 'eur'  # Euro
CRYPTO_MODULE_CONFIG['fiat'] = 'gbp'  # British Pound
CRYPTO_MODULE_CONFIG['fiat'] = 'jpy'  # Japanese Yen
```

### Why are crypto prices not updating?

Check:
1. **Internet connection** - Test with `ping google.com`
2. **Update interval** - Default is 600 seconds (10 minutes)
3. **CoinGecko API** - May have rate limits or be down
4. **Console errors** - Run manually to see error messages

### Do I need an API key for crypto prices?

No! CoinGecko API is free and doesn't require an API key.

---

## 🌡️ Weather

### Do I need an API key for weather?

Yes, but it's free! Get one at: https://www.weatherapi.com/

Set it as an environment variable:
```bash
export WEATHER_API_KEY=your_key_here
```

See [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) for setup methods.

### How does weather location detection work?

The weather module automatically detects your location using your IP address. No manual configuration needed!

### Can I set a specific location for weather?

Currently, weather uses auto-detection via IP. To add custom location support, you'd need to modify `modules/weather_time.py`.

See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for module customization.

### Weather module is not working. What should I check?

1. **API key is set:**
   ```bash
   echo $WEATHER_API_KEY
   ```

2. **Module is enabled:**
   ```python
   WEATHER_MODULE_CONFIG['enabled'] = True  # in config.py
   ```

3. **Internet connection works**

4. **Test API manually:**
   ```bash
   curl "http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=auto:ip"
   ```

---

## 🖥️ Hardware & LCD

### What if my LCD has a different I2C address?

Change the address in `config.py`:

```python
LCD_CONFIG['address'] = 0x3F  # Change from default 0x27 if needed
```

To find your LCD address, run:
```bash
sudo i2cdetect -y 1
```

Common addresses: `0x27` or `0x3F`

### How do I enable I2C on my Raspberry Pi?

```bash
sudo raspi-config
# → Interface Options → I2C → Enable
```

Then reboot:
```bash
sudo reboot
```

> 📖 **For complete I2C setup instructions:**  
> See **[I2C_SETUP.md](I2C_SETUP.md)** for comprehensive step-by-step guide

### LCD is not displaying anything. What should I check?

1. **I2C is enabled** - Run `sudo raspi-config` and enable I2C interface
2. **Required libraries installed** - Run `sudo apt-get install -y i2c-tools python3-smbus`
3. **LCD is connected properly** - Check all 4 wires (GND, VCC, SDA, SCL)
4. **I2C address is correct** - Use `sudo i2cdetect -y 1` to find address
5. **LCD has power** - Check backlight is on (means VCC and GND connected)
6. **Contrast adjustment** - Turn the potentiometer on LCD module
7. **Verify I2C device** - Run `ls /dev/i2c*` (should show `/dev/i2c-1`)

> 📖 **For complete troubleshooting guide:**  
> See **[I2C_SETUP.md](I2C_SETUP.md)** for comprehensive solutions to all I2C issues

### Can I use a different LCD size?

The code is optimized for 16x2 LCD. For other sizes (20x4, etc.), you'd need to:
1. Update `LCD_CONFIG` in `config.py`
2. Modify display methods in each module

See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for module customization.

### What hardware do I need?

**Required:**
- Raspberry Pi (any model with GPIO - tested on Pi 4)
- 16x2 LCD with I2C interface (PCF8574 or compatible)
- 4 jumper wires (female-to-female recommended)
- Power supply for Raspberry Pi (2.5A+ recommended)

**Required Software:**
- I2C enabled on Raspberry Pi (via raspi-config)
- `i2c-tools` and `python3-smbus` libraries
- `RPLCD` Python library

> 📖 **For complete hardware setup with wiring diagrams:**  
> See the [Hardware Setup](../README.md#-hardware-setup) section in README.md
- Internet connection

No additional sensors or components needed!

---

## 🔄 Service Management

### How do I check if the service is running?

```bash
sudo systemctl status crypto_ticker.service
```

Look for "active (running)" in the output.

### How do I start/stop/restart the service?

```bash
sudo systemctl start crypto_ticker.service    # Start
sudo systemctl stop crypto_ticker.service     # Stop
sudo systemctl restart crypto_ticker.service  # Restart
```

### Where are the logs?

```bash
# Follow logs in real-time
sudo journalctl -u crypto_ticker.service -f

# View last 50 lines
sudo journalctl -u crypto_ticker.service -n 50

# View logs since today
sudo journalctl -u crypto_ticker.service --since today
```

### How do I enable autostart on boot?

```bash
sudo systemctl enable crypto_ticker.service
```

To disable:
```bash
sudo systemctl disable crypto_ticker.service
```

### The service won't start. What should I check?

1. **Check service status:**
   ```bash
   sudo systemctl status crypto_ticker.service
   ```

2. **Check logs:**
   ```bash
   sudo journalctl -u crypto_ticker.service -n 50
   ```

3. **Verify file paths in service file**
4. **Check Python path and virtual environment**
5. **Ensure permissions are correct**

See [SYSTEMD_SETUP.md](SYSTEMD_SETUP.md) for complete troubleshooting.

### Can I run it without systemd?

Yes! Simply run manually:
```bash
cd /path_to_folder/rasp-crypto-ticker
python main.py
```

---

## 🔧 Customization

### Can I create my own custom module?

Yes! The modular architecture makes it easy to add custom modules.

See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for complete guide with:
- Step-by-step tutorial
- Module template
- Examples (stocks, news, sports, etc.)

### How do I modify an existing module?

1. Edit the module file in `modules/` directory
2. Test changes: `python main.py`
3. Restart service: `sudo systemctl restart crypto_ticker.service`

See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for module architecture details.

### Can I change the display format?

Yes! Edit the `display()` method in the module file. For example, to change crypto display:

Edit `modules/crypto_ticker.py`, find the `_display_crypto()` method and customize the LCD output.

### Can I add more than 3 cryptocurrencies?

Absolutely! Add as many as you want:

```python
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'ADA': 'cardano',
    'DOT': 'polkadot',
    'AVAX': 'avalanche-2',
    'LINK': 'chainlink',
    'MATIC': 'matic-network',
    # ... add more
}
```

**Note:** More coins = longer cycle time (each displays for 10 seconds by default).

---

## 🐛 Troubleshooting

### Module is not displaying. What should I check?

1. **Module is enabled:**
   ```python
   MODULE_CONFIG['enabled'] = True  # in config.py
   ```

2. **Module is in display order:**
   ```python
   MODULE_ORDER = ['weather', 'crypto']  # in config.py
   ```

3. **No errors in console** - Run manually to check
4. **API keys are set** (for weather module)

### Display is too fast/slow. How do I adjust it?

**For individual modules:**
```python
WEATHER_MODULE_CONFIG['display_duration'] = 15  # seconds
```

**Calculation:**
- Weather: 3 screens × 15s = 45 seconds
- Crypto: 3 coins × 10s = 30 seconds
- **Total cycle: 75 seconds**

### Data seems old. Why isn't it updating?

Check the `update_interval` settings:
```python
WEATHER_MODULE_CONFIG['update_interval'] = 600  # 10 minutes
CRYPTO_MODULE_CONFIG['update_interval'] = 600   # 10 minutes
```

Data is cached for this duration. Increase update frequency if needed (be mindful of API limits).

### I see error messages about API limits

**CoinGecko:** Free tier allows 10-50 calls/minute. Default update (600s) is safe.

**WeatherAPI:** Free tier allows ~1M calls/month. Default update (600s) uses ~4,320/month.

Solution: Increase `update_interval` to reduce API calls.

### The LCD shows garbage characters

This usually means:
1. **I2C address is wrong** - Check with `i2cdetect -y 1`
2. **Loose connections** - Check wiring
3. **Initialization failed** - Restart the application

### Application crashes on startup

1. **Check Python version:** Python 3.x required
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Check LCD connection:** `i2cdetect -y 1` should show device
4. **Review error logs:** Run manually to see full error

---

## 📊 Performance

### How much CPU/RAM does it use?

Very little! On a Raspberry Pi 3/4:
- **CPU:** < 5% (mostly idle)
- **RAM:** ~50-100 MB
- **Network:** Minimal (API calls every 10 minutes)

### Can I run other applications alongside it?

Yes! The ticker is lightweight and won't interfere with other applications.

### Does it slow down my Raspberry Pi?

No. The application is very efficient:
- Updates are infrequent (every 10 minutes)
- Display rotation is simple
- No heavy processing required

### What about power consumption?

Minimal. The LCD backlight uses more power than the code. Total power draw is negligible on a Pi.

---

## 🔐 Security & Privacy

### Does it send my data anywhere?

No. The application only:
- Fetches weather data (using your IP for location)
- Fetches cryptocurrency prices (public data)
- Displays locally on your LCD

No analytics, no tracking, no data collection.

### Is my Weather API key secure?

API keys are stored as environment variables, not in code. This is a security best practice.

For additional security, you can:
1. Set restrictive file permissions on `launcher.sh`
2. Use systemd environment files
3. Avoid committing `.env` files to git

See [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) for environment variable setup.

### Can others access my ticker remotely?

Only if you explicitly expose it. By default:
- Runs locally on your Pi
- No network services listening
- No remote access

To enable remote access to your Raspberry Pi (SSH, VNC, etc.), see the [official Raspberry Pi remote access guide](https://www.raspberrypi.com/documentation/computers/remote-access.html).

---

## 📈 Advanced Usage

### Can I run multiple instances with different configs?

Yes! Create copies of the project directory with different `config.py` files. Use different systemd services for each.

### Can I log data to a file/database?

Not built-in, but you can modify the modules to add logging. See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for customization.

### Can I control it via web interface?

Not built-in. You could create a web interface that modifies `config.py` and restarts the service.

### Can I use it without a physical LCD (for testing)?

Yes! Create a mock LCD class for testing. Example in [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md).

### How do I update to the latest version?

```bash
cd /path_to_folder/rasp-crypto-ticker
git pull origin main
sudo systemctl restart crypto_ticker.service
```

---

## 🆘 Getting Help

### Where can I find more documentation?

- **Configuration:** [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)
- **Architecture & Modules:** [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md)
- **Service Setup:** [SYSTEMD_SETUP.md](SYSTEMD_SETUP.md)
- **Quick Start:** [README.md](../README.md)

### I found a bug. What should I do?

1. Check logs: `sudo journalctl -u crypto_ticker.service -n 100`
2. Test manually: `python main.py`
3. Review configuration: `config.py`
4. Check this FAQ for similar issues

### How do I report an issue?

Include:
- Error messages from logs
- Your configuration (remove API keys!)
- Hardware details (Pi model, LCD type)
- Steps to reproduce

### Can I contribute to the project?

Yes! The modular architecture makes it easy to add features. Fork the repository and submit pull requests.

---

## 📝 Common Scenarios

### Scenario: I only want to see crypto prices

```python
# In config.py
WEATHER_MODULE_CONFIG['enabled'] = False
CRYPTO_MODULE_CONFIG['enabled'] = True

MODULE_ORDER = ['crypto']
```

### Scenario: Quick rotation through all modules

```python
# In config.py
WEATHER_MODULE_CONFIG['display_duration'] = 5
CRYPTO_MODULE_CONFIG['display_duration'] = 5
```

Result: 7 screens × 5 seconds = 35-second cycle

### Scenario: Show crypto multiple times

```python
# In config.py
MODULE_ORDER = ['crypto', 'weather', 'crypto']
```

### Scenario: Track my crypto portfolio

```python
# In config.py
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'ADA': 'cardano',
    'DOT': 'polkadot',
    'LINK': 'chainlink',
    'AVAX': 'avalanche-2',
    'MATIC': 'matic-network',
}
```

### Scenario: Weather focus with minimal crypto

```python
# In config.py
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',  # Just BTC
}

MODULE_ORDER = ['weather', 'crypto']
```

---

## 🔗 Related Documentation

- **I2C Setup**: See [I2C_SETUP.md](I2C_SETUP.md)
- **Architecture & Modules**: See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md)
- **Configuration Guide**: See [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)
- **Systemd Service**: See [SYSTEMD_SETUP.md](SYSTEMD_SETUP.md)
- **Quick Start**: See [README.md](../README.md)

---

**Back to main README**: [README.md](../README.md)

