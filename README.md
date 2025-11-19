# Raspberry Pi Clock & Crypto Ticker

A display system for Raspberry Pi with LCD screen that shows cryptocurrency prices, weather, and time information.

**Version**: 2.0.0

---

## 🎯 Features

- 🌡️ **Weather & Time Module**: Displays temperature, feels-like temperature, and weather conditions (all with current time)
- 💰 **Crypto Module**: Displays cryptocurrency prices (BTC, ETH, SOL) with 24h change

All modules can be independently enabled/disabled and customized.

---

## 📁 Project Structure

```
rasp-crypto-ticker/
│
├── 🚀 main.py                   ← Entry point
│   ├── Uses config.py for settings
│   ├── Imports modules from modules/ directory
│   ├── init_lcd()
│   ├── establish_connection()
│   ├── initialize_modules()
│   ├── display_module_status()
│   └── main()
│
├── ⚙️  config.py                 ← Configuration file
└── 📦 modules/                   ← Module directory
    ├── __init__.py
    │
    ├── 🏗️  base_module.py        ← BASE CLASS
    │   └── BaseModule (Abstract)
    │       ├── fetch_data()      [abstract]
    │       ├── display()         [abstract]
    │       ├── should_update_data()
    │       ├── update_data()
    │       ├── is_enabled()
    │       └── get_display_count()
    │
    ├── 🌡️  weather_time.py       ← WEATHER & TIME MODULE
    │   └── WeatherModule(BaseModule)
    │       ├── fetch_data()      → WeatherAPI
    │       ├── display()         → 3 screens
    │       ├── _print_clock()
    │       └── _lcd_write_string_centered()
    │
    └── 💰 crypto_module.py       ← CRYPTO MODULE
        └── CryptoModule(BaseModule)
            ├── fetch_data()      → CoinGecko API
            ├── display()         → N screens (1 per coin)
            └── _display_crypto()
```

### File Usage Summary

| File/Directory | Purpose |
|----------------|---------|
| `main.py` | Application entry point |
| `config.py` | Configuration file (all settings) |
| `modules/` | Module files (weather_time, crypto) |

---

## 🔄 Module Inheritance Hierarchy

```
        BaseModule (Abstract)
                │
        ┌───────┴───────┐
        │               │
WeatherModule     CryptoModule
        │               │
    4 screens       N screens
```

---

## 🚀 Quick Start

### Installation

1. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variable for weather API:**
```bash
export WEATHER_API_KEY="your_api_key_here"
```

3. **Run the project:**

```bash
python main.py
```

> 💡 **Tip**: All configuration is managed through `config.py`. See the [Configuration](#️-configuration) section for details.

---

## 🔄 Running on Boot (Autostart)

To run the crypto ticker automatically when your Raspberry Pi boots:

**Quick Setup:**
```bash
# 1. Create systemd service file
sudo nano /etc/systemd/system/crypto_ticker.service

# 2. Enable and start
sudo systemctl enable crypto_ticker.service
sudo systemctl start crypto_ticker.service

# 3. Check status
sudo systemctl status crypto_ticker.service
```

📖 **For complete setup instructions, service management, and troubleshooting:**  
See **[SYSTEMD_SERVICE.md](docs/SYSTEMD_SERVICE.md)** for detailed documentation.

**Quick commands:**
```bash
sudo systemctl start crypto_ticker.service    # Start
sudo systemctl stop crypto_ticker.service     # Stop
sudo systemctl restart crypto_ticker.service  # Restart
sudo journalctl -u crypto_ticker.service -f   # View logs
```

## ⚙️ Configuration

All settings are managed in **`config.py`**.

📖 **For complete configuration guide with all options and examples:**  
See **[CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)** for detailed documentation.

### Quick Configuration Guide

**1. Enable/Disable Modules**
```python
# Edit config.py
WEATHER_MODULE_CONFIG['enabled'] = True   # or False
CRYPTO_MODULE_CONFIG['enabled'] = True
```

**2. Add Cryptocurrencies**
```python
# Edit config.py - CRYPTO_MODULE_CONFIG
'symbols': {
    'BTC': 'bitcoin',      # Short acronyms for 16x2 LCD display
    'ETH': 'ethereum',
    'ADA': 'cardano',
}
# Find CoinGecko IDs at: https://api.coingecko.com/api/v3/coins/list
```

**3. Change Display Order**
```python
# Edit config.py
MODULE_ORDER = ['crypto', 'weather']  # Any order you want
```

**4. Adjust Timing**
```python
# Edit config.py
WEATHER_MODULE_CONFIG['display_duration'] = 10  # seconds per screen
CRYPTO_MODULE_CONFIG['update_interval'] = 600   # seconds between updates
```

> 💡 **Tip**: See [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md) for complete guide

---

## 📦 Modules

Two built-in modules are available:

| Module | Displays | API | File |
|--------|----------|-----|------|
| **Weather & Time** | Temperature, Feels Like, Condition (all with time) | WeatherAPI | `modules/weather_time.py` |
| **Crypto** | Price + 24h change per coin | CoinGecko | `modules/crypto_module.py` |

All modules can be enabled/disabled in `config.py`.

📖 **For detailed module information and creating custom modules:**  
See **[MODULES_GUIDE.md](docs/MODULES_GUIDE.md)** for complete documentation.

---

## 📺 LCD Display Examples

**Weather & Time:** Temperature, Feels Like, Condition (all show current time)  
**Crypto:** Symbol, Price, 24h Change  

Example display (Crypto):
```
┌────────────────┐
│14:30      +5.2%│ ← Time + 24h Change
│BTC:     $95432 │ ← Symbol + Price
└────────────────┘
```

> See [MODULES_GUIDE.md](docs/MODULES_GUIDE.md) for all display formats

---

## 🎯 Configuration Examples

**Only show crypto:**
```python
# In config.py
WEATHER_MODULE_CONFIG['enabled'] = False
CRYPTO_MODULE_CONFIG['enabled'] = True
```

**Add more coins:**
```python
# Use short acronyms (3-4 chars work best on LCD)
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'ADA': 'cardano',
    'DOT': 'polkadot',
}
```

**Change display order:**
```python
MODULE_ORDER = ['crypto', 'weather']  # Crypto first
```

**Adjust timing:**
```python
CRYPTO_MODULE_CONFIG['display_duration'] = 15  # 15 seconds per coin
```

> 💡 See `config.py` for all available options and detailed documentation

---

## 🛠️ Creating Custom Modules

Want to add your own module (stocks, news, sports, etc.)?

The modular architecture makes it easy to extend with custom modules.

📖 **Complete guide with examples and templates:**  
See **[MODULES_GUIDE.md](docs/MODULES_GUIDE.md)** for step-by-step instructions.

---

## 💻 Hardware Requirements

- Raspberry Pi (any model with I2C)
- 16x2 LCD display with I2C interface (PCF8574)
- LCD connected to I2C address 0x27

---

## 🐛 Troubleshooting

### Module not displaying?
- Check `enabled` is set to `True` in config
- Verify API keys are set (for weather)
- Check console output for errors

### Data not updating?
- Check `update_interval` setting
- Verify internet connection
- Check API rate limits

### Display duration too short/long?
- Adjust `display_duration` in module config
- Default is 10 seconds per screen

### LCD not working?
- Verify I2C is enabled on Raspberry Pi
- Check LCD address (should be 0x27)
- Test with `i2cdetect -y 1`

---

## ❓ FAQ

Have questions? Check the comprehensive FAQ for answers!

📖 **Complete FAQ with 50+ questions and answers:**  
See **[FAQ.md](docs/FAQ.md)** for detailed help.

**Quick answers:**
- **Which file to run?** → `python main.py`
- **Which file to edit?** → `config.py`
- **Enable/disable modules?** → Set `enabled` in `config.py`
- **Add cryptocurrencies?** → Edit `symbols` in `config.py`
- **Service not starting?** → Check logs with `journalctl -u crypto_ticker.service`

> See [FAQ.md](docs/FAQ.md) for configuration, troubleshooting, customization, and more

---

## 📚 Additional Resources

- **Project Documentation**:
  - [FAQ.md](docs/FAQ.md) - Frequently asked questions (50+ Q&A)
  - [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md) - Complete configuration guide
  - [MODULES_GUIDE.md](docs/MODULES_GUIDE.md) - Module details and custom module creation
  - [SYSTEMD_SERVICE.md](docs/SYSTEMD_SERVICE.md) - Systemd service setup and management
- **External Resources**:
  - WeatherAPI: https://www.weatherapi.com/
  - CoinGecko API: https://www.coingecko.com/api
  - RPLCD Documentation: https://rplcd.readthedocs.io/
  - Raspberry Pi I2C Setup: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

---

## 📄 License

MIT

---

**Enjoy your crypto ticker! 🚀**
