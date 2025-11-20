# Configuration Guide

Complete guide for configuring the Raspberry Pi Crypto Ticker.

---

## 📋 Overview

All application settings are managed in **`config.py`** - a single, centralized configuration file.

**Key Features:**
- ✅ Single configuration file (no separate JSON)
- ✅ Enable/disable modules independently
- ✅ Customize display timing and order
- ✅ Add/remove cryptocurrencies easily
- ✅ Configure hardware settings
- ✅ Environment variable support

---

## 📂 Configuration File Location

```
/path_to_folder/rasp-crypto-ticker/config.py
```

Edit this file to customize all application behavior.

---

## 🎯 Quick Configuration Tasks

### Enable/Disable Modules

**Disable Weather Module:**
```python
WEATHER_MODULE_CONFIG = {
    'enabled': False,  # Changed from True
    # ... rest of config
}
```

**Enable Only Crypto:**
```python
WEATHER_MODULE_CONFIG['enabled'] = False
CRYPTO_MODULE_CONFIG['enabled'] = True
```

### Add Cryptocurrencies

**Add Cardano, Polkadot, and Avalanche:**
```python
CRYPTO_MODULE_CONFIG = {
    'enabled': True,
    'symbols': {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'SOL': 'solana',
        'ADA': 'cardano',       # ← New
        'DOT': 'polkadot',      # ← New
        'AVAX': 'avalanche-2',  # ← New
    },
    # ... rest of config
}
```

**Important**: Use short acronyms (3-4 chars) for 16x2 LCD display!

### Change Display Order

**Show Crypto First:**
```python
MODULE_ORDER = ['crypto', 'weather']
```

**Crypto Only, Multiple Times:**
```python
MODULE_ORDER = ['crypto', 'crypto', 'crypto']
```

### Adjust Display Timing

**Faster Display (5 seconds per screen):**
```python
WEATHER_MODULE_CONFIG['display_duration'] = 5
CRYPTO_MODULE_CONFIG['display_duration'] = 5
```

**Slower Updates (30 minutes):**
```python
WEATHER_MODULE_CONFIG['update_interval'] = 1800
CRYPTO_MODULE_CONFIG['update_interval'] = 1800
```

---

## ⚙️ Configuration Sections

### 1. LCD Hardware Configuration

```python
LCD_CONFIG = {
    'address': 0x27,        # I2C address
    'port': 1,              # I2C port
    'cols': 16,             # LCD columns
    'rows': 2,              # LCD rows
    'dotsize': 8,           # Character dot size
    'max_size': 16          # Max characters per line
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `address` | hex | `0x27` | I2C address of LCD (check with `i2cdetect -y 1`) |
| `port` | int | `1` | I2C port (1 for newer Pi, 0 for old models) |
| `cols` | int | `16` | Number of columns (16 for 16x2 display) |
| `rows` | int | `2` | Number of rows (2 for 16x2 display) |
| `dotsize` | int | `8` | Character dot matrix size |
| `max_size` | int | `16` | Maximum characters per line |

**Common I2C Addresses:**
- `0x27` - Most common (default)
- `0x3F` - Alternative common address
- Check with: `i2cdetect -y 1`

**Troubleshooting:**
```bash
# Find your LCD I2C address
sudo i2cdetect -y 1

# Enable I2C if not working
sudo raspi-config
# → Interface Options → I2C → Enable
```

---

### 2. Weather Module Configuration

```python
WEATHER_MODULE_CONFIG = {
    'enabled': True,
    'api_key': os.getenv('WEATHER_API_KEY'),
    'update_interval': 600,
    'display_duration': 10,
    'timeout': 10,
    'lcd_max_size': LCD_CONFIG['max_size']
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | `True` | Enable/disable weather module |
| `api_key` | str | env var | WeatherAPI key from `WEATHER_API_KEY` |
| `update_interval` | int | `600` | Seconds between API updates (10 min) |
| `display_duration` | int | `10` | Seconds to display each screen |
| `timeout` | int | `10` | API request timeout (seconds) |
| `lcd_max_size` | int | `16` | LCD character width |

**Display Screens:**
1. Temperature (°C)
2. Feels Like temperature (°C)
3. Weather condition

**Total Display Time:** 3 screens × 10 seconds = **30 seconds**

**API Key Setup:**

1. Get free API key from: https://www.weatherapi.com/
2. Set environment variable:

```bash
# In launcher.sh
export WEATHER_API_KEY=your_api_key_here

# Or in systemd service
Environment="WEATHER_API_KEY=your_api_key_here"

# Or system-wide
echo 'export WEATHER_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

**Features:**
- Auto-detects location via IP address
- Shows temperature in Celsius
- Displays "feels like" temperature
- Shows weather condition (Sunny, Cloudy, etc.)
- Updates every 10 minutes (configurable)

**API Usage:**
- Free tier: ~1M calls/month
- Default update: 600 seconds = 144 calls/day
- Monthly: ~4,320 calls (well within free limit)

---

### 3. Crypto Module Configuration

```python
CRYPTO_MODULE_CONFIG = {
    'enabled': True,
    'symbols': {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'SOL': 'solana',
    },
    'fiat': 'usd',
    'update_interval': 600,
    'display_duration': 10,
    'timeout': 10,
    'lcd_max_size': LCD_CONFIG['max_size']
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | `True` | Enable/disable crypto module |
| `symbols` | dict | See below | Cryptocurrency mapping (acronym: id) |
| `fiat` | str | `'usd'` | Display currency (usd, eur, gbp, etc.) |
| `update_interval` | int | `600` | Seconds between API updates (10 min) |
| `display_duration` | int | `10` | Seconds per cryptocurrency |
| `timeout` | int | `10` | API request timeout (seconds) |
| `lcd_max_size` | int | `16` | LCD character width |

**Display Format (per coin):**
```
Row 0: 14:30      +5.2%  (time + 24h change)
Row 1: BTC:     $95432  (acronym + price)
```

**Total Display Time:** N coins × 10 seconds (N = number in `symbols`)

**Adding Cryptocurrencies:**

```python
'symbols': {
    # Format: 'ACRONYM': 'coingecko-id'
    
    # Top Cryptocurrencies
    'BTC': 'bitcoin',           # Bitcoin
    'ETH': 'ethereum',          # Ethereum
    'SOL': 'solana',            # Solana
    'BNB': 'binancecoin',       # Binance Coin
    'XRP': 'ripple',            # Ripple
    'ADA': 'cardano',           # Cardano
    'DOGE': 'dogecoin',         # Dogecoin
    'DOT': 'polkadot',          # Polkadot
    'MATIC': 'matic-network',   # Polygon
    'LINK': 'chainlink',        # Chainlink
    'AVAX': 'avalanche-2',      # Avalanche
    'ATOM': 'cosmos',           # Cosmos
    'UNI': 'uniswap',           # Uniswap
    'XLM': 'stellar',           # Stellar
    'ALGO': 'algorand',         # Algorand
    
    # DeFi Tokens
    'AAVE': 'aave',             # Aave
    'MKR': 'maker',             # Maker
    'COMP': 'compound-governance-token',  # Compound
    'SNX': 'synthetix-network-token',     # Synthetix
    'CRV': 'curve-dao-token',   # Curve
    
    # Layer 2
    'ARB': 'arbitrum',          # Arbitrum
    'OP': 'optimism',           # Optimism
    
    # Memecoins
    'SHIB': 'shiba-inu',        # Shiba Inu
    'PEPE': 'pepe',             # Pepe
    'FLOKI': 'floki',           # Floki
}
```

**Important Notes:**

1. **Use Short Acronyms**: 3-4 characters work best on 16x2 LCD
   - ✅ Good: `BTC`, `ETH`, `SOL`, `ADA`
   - ❌ Bad: `BITCOIN`, `ETHEREUM` (too long)

2. **CoinGecko ID Format**:
   - Most coins: lowercase name (`bitcoin`, `ethereum`)
   - Some coins have suffixes: `avalanche-2`, `matic-network`
   - Find IDs at: https://api.coingecko.com/api/v3/coins/list

3. **Display Order**: Displayed in the order listed in config

4. **API Limits**:
   - Free tier: 10-50 calls/minute
   - Default: 600 seconds = 1 call per 10 minutes
   - Safe for any number of coins

**Fiat Currency Options:**

```python
'fiat': 'usd'  # US Dollar ($)
'fiat': 'eur'  # Euro (€)
'fiat': 'gbp'  # British Pound (£)
'fiat': 'jpy'  # Japanese Yen (¥)
'fiat': 'aud'  # Australian Dollar
'fiat': 'cad'  # Canadian Dollar
'fiat': 'chf'  # Swiss Franc
'fiat': 'cny'  # Chinese Yuan
'fiat': 'inr'  # Indian Rupee
'fiat': 'krw'  # Korean Won
# ... and many more
```

**API Usage:**
- Free API (no key required)
- Endpoint: `https://api.coingecko.com/api/v3/simple/price`
- Rate limit: 10-50 calls/minute
- Default update: 600 seconds (well within limits)

---

### 5. Application Configuration

```python
APP_CONFIG = {
    'version': 'V2.0.0',
    'connection_timeout': 10,
    'retry_delay': 5
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `version` | str | `'V2.0.0'` | Application version (displayed on startup) |
| `connection_timeout` | int | `10` | Network connection timeout (seconds) |
| `retry_delay` | int | `5` | Delay before retry on error (seconds) |

**Features:**
- Version displayed on LCD during startup
- Automatic retry on network errors
- Connection timeout prevents hanging

---

### 6. Module Display Order

```python
MODULE_ORDER = ['weather', 'crypto']
```

**Description:**
Determines the sequence in which modules are displayed in the main loop.

**Examples:**

```python
# Default order
MODULE_ORDER = ['weather', 'clock', 'crypto']

# Crypto first
MODULE_ORDER = ['crypto', 'weather']

# Only crypto
MODULE_ORDER = ['crypto']

# Crypto between other modules
MODULE_ORDER = ['weather', 'crypto', 'clock', 'crypto']

# Custom sequence
MODULE_ORDER = ['crypto', 'crypto', 'weather']
```

**Notes:**
- Modules display in the order listed
- Can repeat modules in the list
- Disabled modules are automatically skipped
- Order affects total cycle time

---

## 📊 Configuration Examples

### Example 1: Crypto-Only Display

```python
# Disable other modules
WEATHER_MODULE_CONFIG['enabled'] = False
CRYPTO_MODULE_CONFIG['enabled'] = True

# Add more cryptocurrencies
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'ADA': 'cardano',
    'DOT': 'polkadot',
    'AVAX': 'avalanche-2',
}

# Faster updates
CRYPTO_MODULE_CONFIG['update_interval'] = 300  # 5 minutes

# Display order
MODULE_ORDER = ['crypto']
```

**Result:** 6 crypto screens, 10 seconds each = 60-second cycle

---

### Example 2: Quick Rotation

```python
# Enable all modules
WEATHER_MODULE_CONFIG['enabled'] = True
CRYPTO_MODULE_CONFIG['enabled'] = True

# Fast display
WEATHER_MODULE_CONFIG['display_duration'] = 5
CRYPTO_MODULE_CONFIG['display_duration'] = 5

# Default order
MODULE_ORDER = ['weather', 'crypto']
```

**Result:** 7 screens × 5 seconds = 35-second cycle

---

### Example 3: Weather Focus

```python
# Enable all
WEATHER_MODULE_CONFIG['enabled'] = True
CRYPTO_MODULE_CONFIG['enabled'] = True

# Weather first, crypto minimal
CRYPTO_MODULE_CONFIG['symbols'] = {
    'BTC': 'bitcoin',
}

# Custom order
MODULE_ORDER = ['weather', 'crypto']
```

**Result:** Weather (30s) + BTC (10s) = 40-second cycle

---

### Example 4: Dual Currency Portfolio

```python
# Enable crypto only
WEATHER_MODULE_CONFIG['enabled'] = False
CRYPTO_MODULE_CONFIG['enabled'] = True

# Portfolio tracking
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

# Frequent updates
CRYPTO_MODULE_CONFIG['update_interval'] = 180  # 3 minutes
CRYPTO_MODULE_CONFIG['display_duration'] = 8   # 8 seconds each

MODULE_ORDER = ['crypto']
```

**Result:** 8 coins × 8 seconds = 64-second cycle, updates every 3 minutes

---

## 🔧 Advanced Configuration

### Custom Module Order Patterns

**Alternating Pattern:**
```python
MODULE_ORDER = ['crypto', 'weather', 'crypto']
```

**Emphasis Pattern:**
```python
# Show crypto 3 times, others once
MODULE_ORDER = ['crypto', 'crypto', 'crypto', 'weather']
```

**Repeated Cycle:**
```python
# Repeat the sequence
MODULE_ORDER = ['weather', 'crypto'] * 3  # Repeats 3 times
```

### Dynamic Display Duration

**Based on Module:**
```python
# Quick info modules
CRYPTO_MODULE_CONFIG['display_duration'] = 5

# Detailed info modules
WEATHER_MODULE_CONFIG['display_duration'] = 15
```

### Update Frequency Optimization

**Network-Friendly:**
```python
# Reduce API calls
WEATHER_MODULE_CONFIG['update_interval'] = 1800  # 30 minutes
CRYPTO_MODULE_CONFIG['update_interval'] = 900    # 15 minutes
```

**Real-Time Focus:**
```python
# Frequent updates
WEATHER_MODULE_CONFIG['update_interval'] = 300  # 5 minutes
CRYPTO_MODULE_CONFIG['update_interval'] = 120   # 2 minutes
```

**Note:** Respect API rate limits!

---

## ⏱️ Timing Calculations

### Total Cycle Time

Formula: `Sum of (Module Screens × Display Duration)`

**Example (Default Config):**
```
Weather: 3 screens × 10s = 30s
Crypto:  3 coins   × 10s = 30s
─────────────────────────────
Total:   6 screens        = 60s
```

### Update vs Display

**Update Interval:** How often data is fetched from APIs
- Weather: Every 600s (10 minutes)
- Crypto: Every 600s (10 minutes)

**Display Duration:** How long each screen shows
- Default: 10 seconds per screen

**Important:** Update interval is independent of display duration!

### Example Scenarios

**Fast Rotation (5s per screen, 3 cryptos):**
```
Total cycle: (3 + 1 + 3) × 5s = 35 seconds
Updates: Every 10 minutes (unchanged)
```

**Slow Rotation (20s per screen, 5 cryptos):**
```
Total cycle: (3 + 1 + 5) × 20s = 180 seconds (3 minutes)
Updates: Every 10 minutes (unchanged)
```

---

## 🌐 Environment Variables

### Setting Environment Variables

**Method 1: In launcher.sh**
```bash
#!/bin/bash
export WEATHER_API_KEY=your_key_here
python main.py
```

**Method 2: In systemd service**
```ini
[Service]
Environment="WEATHER_API_KEY=your_key_here"
```

**Method 3: System-wide**
```bash
echo 'export WEATHER_API_KEY=your_key_here' >> ~/.bashrc
source ~/.bashrc
```

**Method 4: .env file (optional)**
```bash
# Create .env file
echo "WEATHER_API_KEY=your_key_here" > .env

# Load in Python (requires python-dotenv)
from dotenv import load_dotenv
load_dotenv()
```

### Required Variables

| Variable | Required | Module | How to Get |
|----------|----------|--------|------------|
| `WEATHER_API_KEY` | Yes* | Weather | https://www.weatherapi.com/ |

\* Only required if Weather module is enabled

---

## 🐛 Troubleshooting

### Module Not Displaying

**Check:**
1. Module is enabled in config
2. Module in `MODULE_ORDER` list
3. No errors in console output

**Fix:**
```python
# Verify enabled
CRYPTO_MODULE_CONFIG['enabled'] = True

# Verify in order
MODULE_ORDER = ['weather', 'clock', 'crypto']
```

### Weather Module Not Working

**Check:**
1. API key is set correctly
2. Environment variable is exported
3. Internet connection works

**Debug:**
```bash
# Check env var
echo $WEATHER_API_KEY

# Test API manually
curl "http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=auto:ip"
```

### Crypto Prices Not Updating

**Check:**
1. CoinGecko IDs are correct
2. Internet connection works
3. Not hitting API rate limits

**Debug:**
```bash
# Test API manually
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
```

### Display Too Fast/Slow

**Adjust display_duration:**
```python
# Slower (15 seconds per screen)
WEATHER_MODULE_CONFIG['display_duration'] = 15
CRYPTO_MODULE_CONFIG['display_duration'] = 15

# Faster (5 seconds per screen)
WEATHER_MODULE_CONFIG['display_duration'] = 5
CRYPTO_MODULE_CONFIG['display_duration'] = 5
```

### LCD Not Working

**Check hardware config:**
```python
# Try alternative I2C address
LCD_CONFIG['address'] = 0x3F  # Instead of 0x27

# Verify with command
sudo i2cdetect -y 1
```

---

## 📝 Configuration Checklist

Before running, verify:

- [ ] LCD hardware config matches your display
- [ ] I2C address is correct (`i2cdetect -y 1`)
- [ ] Weather API key is set (if module enabled)
- [ ] Cryptocurrency acronyms are short (3-4 chars)
- [ ] CoinGecko IDs are correct
- [ ] Module order is as desired
- [ ] Display durations are reasonable
- [ ] Update intervals respect API limits
- [ ] All enabled modules are in `MODULE_ORDER`

---

## 🔗 Related Documentation

- **I2C Setup**: See [I2C_SETUP.md](I2C_SETUP.md)
- **Architecture & Modules**: See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md)
- **Systemd Service**: See [SYSTEMD_SETUP.md](SYSTEMD_SETUP.md)
- **Frequently Asked Questions**: See [FAQ.md](FAQ.md)
- **Quick Start**: See [README.md](../README.md)

---

## 📚 External API References

- **WeatherAPI**: https://www.weatherapi.com/docs/
- **CoinGecko**: https://www.coingecko.com/api/documentation
- **CoinGecko Coin List**: https://api.coingecko.com/api/v3/coins/list

---

## 💡 Tips and Best Practices

### Performance

1. **Optimize Update Intervals**: Don't update more than necessary
   ```python
   # Good: 10-minute updates
   'update_interval': 600
   
   # Overkill: 30-second updates (wastes API calls)
   'update_interval': 30
   ```

2. **Balance Display Time**: Not too fast, not too slow
   ```python
   # Good: 10 seconds (easy to read)
   'display_duration': 10
   
   # Too fast: Hard to read
   'display_duration': 3
   
   # Too slow: Boring wait
   'display_duration': 30
   ```

3. **Limit Cryptocurrencies**: Too many = long cycle time
   ```python
   # Good: 3-5 coins = 30-50s cycle
   'symbols': {'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana'}
   
   # Too many: 20 coins = 200s cycle (3+ minutes!)
   ```

### Readability

1. **Short Acronyms**: Fit on 16x2 display
   - ✅ `BTC`, `ETH`, `ADA`, `DOT`
   - ❌ `BITCOIN`, `ETHEREUM` (too long)

2. **Consider Cycle Time**: Total time for one complete rotation
   - 30-90 seconds: Good balance
   - < 30 seconds: Too fast
   - > 2 minutes: Too slow

### Maintenance

1. **Comment Your Changes**: Document custom configurations
   ```python
   # Portfolio tracking - emphasis on DeFi tokens
   'symbols': {
       'AAVE': 'aave',
       'UNI': 'uniswap',
       # ...
   }
   ```

2. **Version Control**: Keep backup of working config
   ```bash
   cp config.py config.py.backup
   ```

3. **Test Changes**: Verify before running as service
   ```bash
   python main.py  # Test manually first
   ```

---

**Back to main README**: [README.md](../README.md)

