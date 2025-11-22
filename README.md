# Raspberry Pi Clock & Crypto Ticker

A modular information display system for Raspberry Pi that transforms a 16x2 LCD screen into a smart ticker, continuously cycling through real-time cryptocurrency prices, weather conditions, and time information.

---

## 📖 What This Project Does

This project turns your Raspberry Pi into an always-on information display that shows:

- **📊 Live Cryptocurrency Prices**: Track Bitcoin, Ethereum, Solana, or any cryptocurrency from CoinGecko API, displaying current price and 24-hour change percentage.
- **🌡️ Real-Time Weather**: Automatically detects your location via IP and displays location name, current temperature (configurable Celsius/Fahrenheit), feels-like temperature, and weather conditions using WeatherAPI.
- **😨 Fear & Greed Index**: Market sentiment indicator showing current index value and classification (Extreme Fear to Extreme Greed).
- **₿ Bitcoin Dominance**: Shows Bitcoin's market dominance percentage (% of total crypto market cap).
- **🔄 Altcoin Season Index**: Shows what percentage of top 100 coins outperformed Bitcoin in the last 7 days and 30 days.
- **💎 Market Cap**: Total cryptocurrency market capitalization with 24h change percentage.
- **🕐 Current Date & Time**: Shows the current date and time on each screen.

The display automatically cycles through configured modules, fetching fresh data at regular intervals. Each module can be independently enabled, disabled, and customized to fit your needs.

---

## 💻 Hardware & Software Requirements

**Hardware:**
- Raspberry Pi 4 (or Pi 2/3/Zero W with GPIO)
- 16x2 LCD with I2C adapter (PCF8574)
- 4 jumper wires
- 5V/2.5A+ power supply

**Software:**
- Raspberry Pi OS (Raspbian)
- I2C interface enabled
- Python 3.x
- Required libraries: `i2c-tools`, `python3-smbus`, `RPLCD`


> 📖 **Setup guides:** [Hardware Wiring & Components](#-hardware-setup) | [I2C Configuration](docs/I2C_SETUP.md)

---

## 🖥️ Hardware Context

This project was developed and tested on a **Raspberry Pi 4** with a **16x2 LCD display** equipped with an **I2C adapter module (PCF8574)**. Understanding this hardware setup helps explain several design decisions in the code:

**Why 16x2 LCD?**
- **Compact & Affordable**: 16 characters × 2 rows provide essential information in a small form factor
- **Wide Availability**: One of the most common LCD sizes for DIY projects
- **Low Power**: Ideal for always-on displays

**Why I2C Interface?**
- **Simplified Wiring**: Only 4 wires (VCC, GND, SDA, SCL) instead of 16+ pins
- **Easy Connection**: No complex pin mapping or voltage dividers needed
- **GPIO Conservation**: Frees up Raspberry Pi GPIO pins for other uses
- **Multiple Devices**: I2C bus allows connecting multiple devices on the same pins

**How This Influences the Code:**

1. **Short Cryptocurrency Acronyms**: Due to the 16-character width limitation, the code uses "BTC" instead of "Bitcoin", "ETH" instead of "Ethereum", etc. This is handled in `config.py` with a symbol mapping dictionary.

2. **Screen Cycling Pattern**: With only 2 rows available, information is split across multiple screens that cycle automatically. Each module displays different data on separate screens (e.g., temperature → feels like → condition).

3. **I2C Configuration**: The code requires proper I2C setup and address detection, which is why `config.py` includes LCD I2C address configuration.

**Compatibility**: While tested on Raspberry Pi 4, this project works on any Raspberry Pi model with GPIO pins (Pi 2, 3, 4, Zero W, etc.). The 16x2 LCD with I2C is standard across different manufacturers, though the I2C address may vary (commonly `0x27` or `0x3F`).
 

---

## 🔧 Hardware Setup

### Required Components

**Hardware:**
- **Raspberry Pi 4** (or any model with GPIO: Pi 2, 3, Zero W, etc.)
  - Tested on Pi 4 Model B with 4GB RAM
  - Works with all Pi models that have 40-pin GPIO header
- **16x2 LCD Display with I2C Adapter Module**
  - PCF8574 or PCF8574T I2C backpack (most common)
  - 16 characters × 2 rows (standard HD44780 controller)
  - Typical I2C address: `0x27` or `0x3F`
  - Operating voltage: 5V (powered by Raspberry Pi)
- **Power Supply**: 5V/2.5A+ USB-C for Pi 4 (or appropriate for your model)

### Wiring Diagram

The I2C LCD module simplifies the connection significantly, requiring only 4 wires instead of the traditional 16-pin setup:

```
LCD I2C Module              Raspberry Pi
┌──────────────┐           ┌──────────────────┐
│              │           │                  │
│   GND   ─────┼───────────┼─ Pin 6  (GND)    │
│   VCC   ─────┼───────────┼─ Pin 2  (5V)     │
│   SDA   ─────┼───────────┼─ Pin 3  (SDA)    │
│   SCL   ─────┼───────────┼─ Pin 5  (SCL)    │
│              │           │                  │
└──────────────┘           └──────────────────┘
```

### Pin Connections

| LCD I2C Pin | Raspberry Pi Pin | Pin # | Description |
|-------------|------------------|-------|-------------|
| GND         | Ground           | 6     | Ground connection |
| VCC         | 5V Power         | 2     | Power supply (5V) |
| SDA         | GPIO 2 (SDA)     | 3     | I2C Data line |
| SCL         | GPIO 3 (SCL)     | 5     | I2C Clock line |

**Important Notes:**
- Most I2C LCD modules (PCF8574) have built-in voltage protection and can be connected directly to Raspberry Pi
- The I2C protocol uses only 2 pins (SDA and SCL) plus power, making it much simpler than parallel LCD connections
- Ensure your connections are secure and pins are correctly identified on your LCD module

### Raspberry Pi I2C Setup

> ⚠️ **Critical**: The I2C interface is **disabled by default** on Raspberry Pi. You must enable it before the LCD will work!

**The I2C protocol allows the Raspberry Pi to communicate with the LCD module using only 2 data wires.** Before using this project, you need to:

1. **Enable I2C** on your Raspberry Pi (`raspi-config`)
2. **Install I2C libraries** (`i2c-tools` and `python3-smbus`)
3. **Detect your LCD address** (typically `0x27` or `0x3F`)
4. **Configure the address** in `config.py`

📖 **Complete setup guide:**  
See **[I2C_SETUP.md](docs/I2C_SETUP.md)** for step-by-step instructions, troubleshooting, and technical details.

🔗 **Additional tutorial:**  
[Circuit Basics - Raspberry Pi I2C LCD Setup](https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/)


---

## 🚀 Software Setup & Quick Start

### Installation

> ⚠️ **Prerequisites**: Make sure you completed the [Hardware Setup](#-hardware-setup) section first (I2C enabled, external libraries set)!

**1. Install Python Dependencies:**

```bash
pip install -r requirements.txt
```

**Why this library is needed:**  
- **`RPLCD`**: Python library to control LCD displays via I2C interface.
- **`requests`**: HTTP library for making API calls to CoinGecko, WeatherAPI, and other services.

**2. Set up Weather API Key:**

The weather module requires an API key to fetch weather data. Get your free API key at: https://www.weatherapi.com/

```bash
export WEATHER_API_KEY="your_api_key_here"
```

> **Note:** If you don't want to use the weather module, you can disable it in `config.py` by setting `'enabled': False` in `WEATHER_MODULE_CONFIG`.

**3. Run the project:**

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
See **[SYSTEMD_SETUP.md](docs/SYSTEMD_SETUP.md)** for detailed documentation.


---

## 📁 Project Structure & Architecture

The project follows a **clean, modular architecture** with clear separation between API communication and display logic. This design emphasizes simplicity, maintainability, and extensibility.

### Core Components

```
rasp-crypto-ticker/
├── main.py           ← Entry point (initializes LCD and runs display loop)
├── config.py         ← Centralized configuration (all settings in one file)
│
├── clients/          ← API Client Layer (HTTP communication)
│   ├── weather_api.py          → WeatherAPI endpoint
│   ├── crypto_api.py           → CoinGecko API endpoint
│   ├── fear_greed_api.py       → Fear & Greed Index endpoint
│   ├── market_cap_api.py       → Global market cap endpoint
│   ├── altcoin_season_api.py   → Altcoin Season Index endpoint
│   └── ip_api.py               → external IP address endpoint 
│
├── modules/          ← Display Layer (data presentation)
│   ├── base.py               → Abstract base class (defines module interface)
│   ├── weather_time.py       → Weather & time display module
│   ├── crypto_ticker.py      → Cryptocurrency price ticker module
│   ├── fear_greed.py         → Fear & Greed Index display module
│   ├── alt_season.py         → Altcoin Season module
│   ├── btc_dominance.py      → Bitcoin Dominance module
│   └── market_cap.py         → Total market cap display module
│
├── utils/            ← Utilities (shared helpers and wrappers)
│   ├── cache.py              → Caching utilities
│   ├── lcd.py                → LCD wrapper
│   └── parser.py             → Data formatting
│
└── docs/             ← Documentation (setup guides and references)
```


📖 **For complete architecture and module development guide:**  
See **[ARCHITECTURE_GUIDE.md](docs/ARCHITECTURE_GUIDE.md)** for design patterns, implementation details, and creating custom modules

---

## ⚙️ Configuration

All settings are managed in **`config.py`**.


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

📖 **For complete configuration guide with all options and examples**  
See **[CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)**

---

## 📺 Modules & Display

### Built-in Modules

Six ready-to-use modules are included:

**🌡️ Weather & Time Module**
- Displays: Location, Temperature, Feels Like, Weather Condition
- Shows current time on each screen
- Auto-detects location via IP
- Configurable temperature unit (°C or °F)
- Updates every 10 minutes (configurable)

**💰 Crypto Module**
- Displays: Symbol, Price, 24h Change
- Supports multiple cryptocurrencies
- Updates every 10 minutes (configurable)
- Uses short acronyms (BTC, ETH, SOL) for 16-char display

**😨 Fear & Greed Index Module**
- Displays: Market sentiment index (0-100)
- Classification: Extreme Fear, Fear, Neutral, Greed, Extreme Greed
- Updates every 1 hour (configurable)
- No API key required (Alternative.me public API)

**₿ Bitcoin Dominance Module**
- Displays: Bitcoin's percentage of total crypto market cap
- Status classification: [Very High (≥55%), High (≥50%), Moderate (≥45%), Low (≥40%), Very Low (<40%)]
- Updates every 10 minutes (configurable)
- No API key required (CoinGecko public API)
- Higher dominance often indicates BTC Season

**🔄 Altcoin Season Module**
- Displays: Percentage of top 100 coins outperforming Bitcoin (calculates 7d and 30d)
- Shows two separate screens: Screen 1 (7-day), Screen 2 (30-day)
- Each screen shows: timeframe, percentage, and season classification
- Season thresholds: Alt Season (≥75%), BTC Season (≤25%), Mixed (25-75%)
- Updates every 10 minutes (configurable)
- No API key required (CoinGecko public API)
- **Note:** Data is calculated locally by comparing price changes of top 100 coins vs Bitcoin

**💎 Market Cap Module**
- Displays: Total cryptocurrency market capitalization
- Shows 24h change percentage
- Updates every 10 minutes (configurable)
- No API key required (CoinGecko public API)

### Display Format Examples

**Weather & Time Module (16x2 LCD):**
```
┌────────────────┐
│2025/01/01 14:30│ ← Current date + time
│   Temp: 25°C   │ ← Temperature (also displays feels like & weather condition)
└────────────────┘
```

**Crypto Module (16x2 LCD):**
```
┌────────────────┐
│14:30      +5.2%│ ← Current time + 24h Change
│BTC:      $95432│ ← Symbol + Price
└────────────────┘
```

**Fear & Greed Index Module:**
```
┌────────────────┐
│Fear & Greed Idx│ ← Title (centered)
│  68 - Greed    │ ← Index value + Classification (centered)
└────────────────┘
```

**Bitcoin Dominance Module:**
```
┌────────────────┐
│ BTC Dominance  │ ← Title (centered)
│56% - Very High │ ← Dominance % + Status (centered)
└────────────────┘
```

**Altcoin Season Module:**

```
┌────────────────┐
│Alt Season (07d)│ ← Title + Timeframe (centered)
│ 53% - Mixed    │ ← Percentage + Season (centered)
└────────────────┘
```

**Market Cap Module:**
```
┌────────────────┐
│14:30      +2.5%│ ← Current time + 24h Change
│Mtk. Cap:  $1.2T│ ← Label + Total Market Cap
└────────────────┘
```

### Creating Custom Modules

Want to add your own module (stocks, news, sports, etc.)? The modular architecture makes it easy!

**Steps to create a new module:**
1. Create a new file in `modules/` directory
2. Inherit from `BaseModule` class
3. Implement `fetch_data()` and `display()` methods
4. Add configuration to `config.py`
5. Enable in `MODULE_ORDER`

📖 **Complete guide:** See [ARCHITECTURE_GUIDE.md](docs/ARCHITECTURE_GUIDE.md) for detailed instructions, templates, examples, and best practices.

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
  - [ARCHITECTURE_GUIDE.md](docs/ARCHITECTURE_GUIDE.md) - Project structure, architecture, and module development
  - [I2C_SETUP.md](docs/I2C_SETUP.md) - Complete I2C setup and troubleshooting guide
  - [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md) - Complete configuration guide
  - [SYSTEMD_SETUP.md](docs/SYSTEMD_SETUP.md) - Systemd service setup and management
  - [FAQ.md](docs/FAQ.md) - Frequently asked questions (50+ Q&A)
- **External Resources**:
  - WeatherAPI: https://www.weatherapi.com/
  - CoinGecko API: https://www.coingecko.com/api
  - Fear & Greed Index: https://alternative.me/crypto/fear-and-greed-index/
  - Altcoin Season Index: https://blockchaincenter.net/altcoin-season-index/
  - RPLCD Documentation: https://rplcd.readthedocs.io/
  - Raspberry Pi I2C Setup: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

**Enjoy your ticker! 🚀**
