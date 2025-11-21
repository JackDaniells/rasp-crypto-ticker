# Project Architecture & Module Development Guide

Complete guide covering project structure, architecture patterns, and module development for the Raspberry Pi Crypto Ticker.

---

## 📋 Table of Contents

1. [Project Structure](#-project-structure)
2. [Architecture Overview](#-architecture-overview)
3. [Module System](#-module-system)
4. [Existing Modules](#-existing-modules)
5. [Creating Custom Modules](#️-creating-custom-modules)
6. [Module Template](#-module-template)
7. [Best Practices](#-best-practices)
8. [Debugging](#-debugging)

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
├── 📜 launcher.sh                ← Startup script (for systemd)
├── 📋 requirements.txt           ← Python dependencies
│
├── 📦 modules/                   ← Module directory
│   ├── __init__.py
│   │
│   ├── 🏗️  base.py                ← BASE CLASS
│   │   └── BaseModule (Abstract)
│   │       ├── fetch_data()      [abstract]
│   │       ├── display()         [abstract]
│   │       ├── is_data_ready()
│   │       ├── update_data()
│   │       ├── is_enabled()
│   │       └── get_display_count()
│   │
│   ├── 🌡️  weather.py            ← WEATHER & TIME MODULE
│   │   └── WeatherModule(BaseModule)
│   │       ├── fetch_data()      → WeatherAPI
│   │       ├── display()         → 3 screens
│   │       ├── _print_clock()
│   │       └── _lcd_write_string_centered()
│   │
│   ├── 💰 crypto.py               ← CRYPTO MODULE
│   │   └── CryptoModule(BaseModule)
│   │       ├── fetch_data()      → CoinGecko API
│   │       ├── display()         → N screens (1 per coin)
│   │       └── _display_crypto()
│   │
│   ├── 😨 fear_greed.py           ← FEAR & GREED INDEX MODULE
│   │   └── FearGreedModule(BaseModule)
│   │       ├── fetch_data()      → Alternative.me API
│   │       └── display()         → 1 screen (index + classification)
│   │
│   ├── ₿ btc_dominance.py         ← BTC DOMINANCE MODULE
│   │   └── BtcDominanceModule(BaseModule)
│   │       ├── fetch_data()      → CoinGecko Global API
│   │       ├── display()         → 1 screen (dominance % + status)
│   │       └── _get_status()     → Determines classification from dominance
│   │
│   ├── 🔄 alt_season.py           ← ALTCOIN SEASON MODULE
│   │   └── AltSeasonModule(BaseModule)
│   │       ├── fetch_data()      → CoinGecko API (calculated)
│   │       ├── display()         → 2 screens (7d and 30d, each with % + season)
│   │       ├── _display_screen() → Helper to display single timeframe
│   │       └── _get_season()     → Determines season from index (Alt/BTC/Mixed)
│   │
│   └── 💎 market_cap.py           ← MARKET CAP MODULE
│       └── MarketCapModule(BaseModule)
│           ├── fetch_data()      → CoinGecko Global API
│           ├── display()         → 1 screen (total cap + 24h change)
│           └── _format_market_cap()
│
├── 🔌 clients/                   ← API Client directory
│   ├── __init__.py
│   │
│   ├── 🗃️  cache_utils.py         ← CENTRALIZED CACHING UTILITIES
│   │   ├── DEFAULT_CACHE_DURATION (600 seconds)
│   │   ├── create_cache()        → Creates standardized cache dict
│   │   ├── cached_api_call()     → Generic cache wrapper for all APIs
│   │   ├── is_cache_valid()      → Validates cache freshness
│   │   ├── update_cache()        → Updates cache with new data
│   │   └── get_cache_age()       → Returns cache age in seconds
│   │
│   ├── 🌡️  weather_api.py         ← Weather API client (with caching)
│   ├── 💰 crypto_api.py           ← CoinGecko prices client (with caching)
│   ├── 😨 fear_greed_api.py       ← Fear & Greed API client (with caching)
│   ├── 🌍 coingecko_global_api.py ← Global market data client (with caching)
│   ├── 🔄 altcoin_season_api.py   ← Altcoin Season calculator (with caching)
│   └── 🌐 ip_api.py               ← IP address client (no caching)
│
└── 📚 docs/                      ← Documentation
    ├── ARCHITECTURE_GUIDE.md     ← This file
    ├── I2C_SETUP.md              ← I2C setup guide
    ├── CONFIGURATION_GUIDE.md    ← Complete configuration guide
    ├── SYSTEMD_SETUP.md          ← Systemd service setup
    └── FAQ.md                    ← Frequently asked questions
```

### File and Directory Purpose

| Path | Type | Purpose |
|------|------|---------|
| `main.py` | File | Application entry point, initializes LCD, modules, and main loop |
| `config.py` | File | Centralized configuration for all modules and app settings |
| `launcher.sh` | File | Shell script for launching the application (used by systemd) |
| `requirements.txt` | File | Python package dependencies |
| `modules/` | Directory | Contains all display modules |
| `modules/base.py` | File | Abstract base class for all modules |
| `modules/weather.py` | File | Weather and time display module |
| `modules/crypto.py` | File | Cryptocurrency price display module |
| `modules/fear_greed.py` | File | Fear & Greed Index display module |
| `modules/btc_dominance.py` | File | Bitcoin Dominance module (BTC % of total market cap) |
| `modules/alt_season.py` | File | Altcoin Season module (7d + 30d, 2 screens) |
| `modules/market_cap.py` | File | Total market cap display module |
| `clients/` | Directory | API client functions for external APIs |
| `clients/cache_utils.py` | File | Centralized caching utilities (DEFAULT_CACHE_DURATION, create_cache(), cached_api_call()) |
| `clients/weather_api.py` | File | WeatherAPI client with caching |
| `clients/crypto_api.py` | File | CoinGecko prices client with caching |
| `clients/fear_greed_api.py` | File | Fear & Greed Index client with caching |
| `clients/coingecko_global_api.py` | File | CoinGecko Global API with caching (market cap, BTC dominance, etc) |
| `clients/altcoin_season_api.py` | File | Altcoin Season Index calculator (7d + 30d via CoinGecko) with caching |
| `clients/ip_api.py` | File | IP address client (no caching needed) |
| `utils/` | Directory | Utility functions |
| `utils/__init__.py` | File | Utility functions (format_large_number) |
| `docs/` | Directory | All project documentation |

---

## 🏗️ Architecture Overview

### Core Design Principles

This project follows a **clean, pragmatic architecture** focused on simplicity and reliability:

#### 1. **Separation of Concerns**

**Two-Layer Architecture:**
```
clients/     → API Communication Layer (HTTP requests + caching)
modules/     → Display Layer (presentation logic only)
```

**Benefits:**
- Easy to test (mock clients for unit tests)
- Easy to debug (network issues vs. display issues)
- Easy to extend (new APIs don't affect display code)
- Centralized caching (consistent behavior across all APIs)

#### 2. **Fail-Safe by Design**

**Never Crash Principle:**
```python
# Clients return None on any error
data = get_weather(...)  # Returns dict or None

# Modules use safe access with defaults
temp = data.get('current', {}).get('temp_c', '--')  # Never crashes
```

**Graceful Degradation:**
- Missing data → Show `--` placeholder
- API failure → Keep last good data (configurable retries)
- Network down → Display continues with cached data

#### 3. **Simple Contracts**

**Client Functions:**
- Input: API parameters (keys, endpoints, timeout, cache_duration)
- Output: Data dict or `None` (no exceptions, no error objects)
- Responsibility: HTTP communication and caching
- Caching: All clients use `cache_utils.py` for consistent caching behavior

**Module Functions:**
- Input: Configuration from `config.py`
- Output: None (side effect: updates LCD)
- Responsibility: Display logic only

#### 4. **Configuration Over Code**

All behavior controlled through `config.py`:
- Which modules are enabled
- Update intervals and display durations
- API keys and endpoints
- Error handling parameters (`max_failed_attempts`)

**Result**: Change behavior without editing code.

---

### How Components Work Together

**1. Application Startup (`main.py`)**

```
main()
  │
  ├─→ init_lcd()                    # Initialize LCD display
  │     └─→ CharLCD(i2c_expander)
  │
  ├─→ establish_connection()        # Get device IP
  │     └─→ socket.connect()
  │
  ├─→ initialize_modules()          # Create module instances
  │     ├─→ WeatherModule(lcd, config)
  │     ├─→ CryptoModule(lcd, config)
  │     ├─→ FearGreedModule(lcd, config)
  │     ├─→ AltcoinSeasonModule(lcd, config)
  │     └─→ MarketCapModule(lcd, config)
  │
  ├─→ display_module_status()       # Show enabled modules
  │
  └─→ Main Loop                     # Display cycle
        └─→ for each module in MODULE_ORDER:
              ├─→ module.update_data()    # Fetch if needed
              └─→ module.display()        # Show on LCD
```

**2. Module Lifecycle**

```
Module Creation
  │
  ├─→ __init__(lcd, config)
  │     ├─→ Store LCD reference
  │     ├─→ Store config settings (including update_interval)
  │     └─→ Initialize data = {}
  │
  ├─→ is_data_ready()
  │     ├─→ Check if self.data exists
  │     └─→ Call update_data() if needed
  │
  ├─→ update_data()
  │     ├─→ fetch_data()              # API call (with caching handled by client)
  │     ├─→ Handle errors gracefully
  │     └─→ Store data or keep previous good data
  │
  └─→ display()
        └─→ Show data on LCD (1+ screens)

Note: API clients handle caching internally using cache_utils.py
      Modules pass update_interval as cache_duration to API clients
```

**3. Configuration Flow**

```
config.py
  │
  ├─→ LCD_CONFIG
  │     └─→ Used by: main.py (init_lcd)
  │
  ├─→ WEATHER_MODULE_CONFIG
  │     └─→ Used by: WeatherModule.__init__()
  │
  ├─→ CRYPTO_MODULE_CONFIG
  │     └─→ Used by: CryptoModule.__init__()
  │
  ├─→ APP_CONFIG
  │     └─→ Used by: main.py (main loop)
  │
  └─→ MODULE_ORDER
        └─→ Used by: main.py (display sequence)
```

### Architecture Benefits

**1. Modularity**
- Each module is self-contained
- Easy to add/remove modules
- No module dependencies

**2. Extensibility**
- Create custom modules by inheriting `BaseModule`
- No changes needed to `main.py`
- Just add to `MODULE_ORDER`

**3. Maintainability**
- Single responsibility per file
- Clear separation of concerns
- Easy to debug and test

**4. Configuration**
- Single source of truth (`config.py`)
- No hardcoded values
- Easy to customize

### Centralized Caching System

**Architecture**: All API clients use a centralized caching system via `cache_utils.py`

**Key Components**:
```python
# cache_utils.py provides:
DEFAULT_CACHE_DURATION = 600  # 10 minutes (single source of truth)

create_cache()           # Creates standardized cache structure
cached_api_call()       # Generic wrapper for any API call
is_cache_valid()        # Validates cache freshness
update_cache()          # Updates cache with new data
get_cache_age()         # Returns cache age in seconds
```

**How It Works**:
```
Module                     API Client                Cache Utils
  │                            │                          │
  ├─ fetch_data()              │                          │
  │    └──────────────────────>│                          │
  │      (passes update_       │                          │
  │       interval as          │                          │
  │       cache_duration)      │                          │
  │                            │                          │
  │                            ├─ cached_api_call()       │
  │                            │    └───────────────────> │
  │                            │      (checks cache)      │
  │                            │                          │
  │                            │<─────────────────────────┤
  │                            │   (returns cached or     │
  │                            │    fetches fresh data)   │
  │<───────────────────────────┤                          │
  │    (receives data)         │                          │
```

**Benefits**:
- **Zero Duplication**: Cache logic exists in one place
- **Consistency**: All APIs cache data identically
- **Single Source of Truth**: `DEFAULT_CACHE_DURATION` defined once
- **Easy to Modify**: Change cache behavior for all APIs in one file
- **Testability**: Cache utilities can be unit tested independently

**API Client Implementation Pattern**:
```python
from .cache_utils import create_cache, cached_api_call, DEFAULT_CACHE_DURATION

_cache = create_cache()  # Standardized cache structure

def get_data(timeout=10, cache_duration=DEFAULT_CACHE_DURATION, force_refresh=False):
    def fetch():
        # API-specific fetch logic here
        return data
    
    return cached_api_call(
        cache=_cache,
        fetch_function=fetch,
        cache_duration=cache_duration,
        force_refresh=force_refresh,
        api_name="API Name"
    )
```

**Module Implementation**:
```python
def fetch_data(self):
    """Fetch data from API (caching handled automatically)"""
    return get_api_data(
        timeout=self.timeout,
        cache_duration=self.update_interval  # Pass module's update interval
    )
```

### Key Design Patterns

**1. Template Method Pattern**  
`BaseModule` defines the skeleton (`update_data()`), subclasses implement specific steps (`fetch_data()`).

**2. Strategy Pattern**  
Different modules implement different display strategies, all following the same interface.

**3. Single Responsibility Principle**  
Each module handles one concern (weather, crypto, etc.).

**4. Open/Closed Principle**  
Open for extension (new modules), closed for modification (no changes to base class).

### File Dependencies

```
main.py
  ├─→ imports: config (LCD_CONFIG, MODULE_CONFIGS, APP_CONFIG, MODULE_ORDER)
  ├─→ imports: modules.weather (WeatherModule)
  ├─→ imports: modules.crypto (CryptoModule)
  ├─→ imports: clients.get_ip_address (for connection setup)
  └─→ imports: RPLCD, time

clients/cache_utils.py
  ├─→ exports: DEFAULT_CACHE_DURATION (600 seconds)
  ├─→ exports: create_cache() → creates standardized cache dict
  ├─→ exports: cached_api_call() → generic caching wrapper
  └─→ exports: Helper functions (is_cache_valid, update_cache, get_cache_age)

clients/weather_api.py
  ├─→ imports: requests, cache_utils
  └─→ exports: get_weather(cache_duration=DEFAULT_CACHE_DURATION) → returns dict or None

clients/crypto_api.py
  ├─→ imports: requests, cache_utils
  └─→ exports: get_crypto_prices(cache_duration=DEFAULT_CACHE_DURATION) → returns dict or None

clients/ip_api.py
  ├─→ imports: requests
  └─→ exports: get_ip_address() → returns str or None (no caching)

modules/weather.py
  ├─→ imports: modules.base (BaseModule)
  ├─→ imports: clients.get_weather (API call)
  ├─→ imports: datetime, time (for display)
  └─→ uses: WEATHER_MODULE_CONFIG from config.py

modules/crypto.py
  ├─→ imports: modules.base (BaseModule)
  ├─→ imports: clients.get_crypto_prices (API call)
  ├─→ imports: datetime, time (for display)
  └─→ uses: CRYPTO_MODULE_CONFIG from config.py

modules/base.py
  ├─→ imports: datetime (for update timing)
  └─→ exports: BaseModule (abstract class)

modules/base.py
  ├─→ imports: time
  └─→ uses: No external dependencies

config.py
  └─→ imports: os (for environment variables)
```

---

## 🔄 Module System

### Module Inheritance Hierarchy

```
        BaseModule (Abstract)
                │
                │ Provides common interface:
                │ - fetch_data() [abstract]
                │ - display() [abstract]
                │ - is_data_ready()
                │ - update_data()
                │ - is_enabled()
                │ - get_display_count()
                │
        ┌───────┴───────┐
        │               │
WeatherModule     CryptoModule
        │               │
    3 screens       N screens
   (per cycle)     (1 per coin)
```

### BaseModule (Abstract Base Class)

**File**: `modules/base.py`

**Purpose**: Defines the common interface for all display modules

**Abstract Methods** (must be implemented):
- `fetch_data()` - Fetch data from APIs/sources
- `display()` - Show data on LCD

**Concrete Methods** (provided by base class):
- `is_data_ready()` - Checks if data is available, fetches if needed
- `update_data()` - Fetches and stores new data (with error handling)
- `is_enabled()` - Returns if module is enabled
- `get_display_count()` - Returns number of screens (default 1)

**Properties**:
- `self.name` - Module name
- `self.lcd` - LCD object reference
- `self.config` - Configuration dictionary
- `self.enabled` - Enabled status
- `self.display_duration` - Seconds per screen
- `self.update_interval` - Seconds between updates (passed to API clients for caching)
- `self.data` - Current module data
- `self.consecutive_failures` - Count of consecutive API failures

---

## 📦 Existing Modules

### Weather & Time Module

**File**: `modules/weather.py`

**Features:**
- 4 display screens: Location, Temperature, Feels Like, Weather Condition
- Auto-fetches weather based on IP location
- Configurable temperature unit (Celsius or Fahrenheit)
- Shows current time on each screen
- Centered text display

**Methods:**
- `fetch_data()` - Fetches weather from WeatherAPI
- `display()` - Shows 4 screens (location, temp, sensation, condition)
- `_print_clock()` - Displays date/time on row 0
- `_lcd_write_string_centered()` - Centers text on LCD

**Display Screens:**
1. Location (City, Country) with time on top
2. Temperature (°C or °F) with time on top
3. Feels Like temperature (°C or °F) with time on top
4. Weather condition (e.g., "Sunny", "Cloudy") with time on top

**Configuration:**
```python
WEATHER_MODULE_CONFIG = {
    'enabled': True,
    'api_key': os.getenv('WEATHER_API_KEY'),
    'update_interval': 600,  # 10 minutes
    'display_duration': 10,  # seconds per screen
    'timeout': 10,
    'lcd_max_size': 16,
    'temperature_unit': 'C'  # Options: 'C' or 'F'
}
```

**API**: WeatherAPI (requires API key)  
**Update Frequency**: Every 10 minutes (configurable)

---

### Crypto Module

**File**: `modules/crypto.py`

**Features:**
- Multi-coin support (configurable)
- Shows 24h price change percentage
- Displays price in configured fiat currency
- One screen per cryptocurrency
- Uses short acronyms for 16x2 LCD display

**Methods:**
- `fetch_data()` - Fetches prices from CoinGecko API
- `display()` - Shows each crypto sequentially
- `_display_crypto()` - Displays single crypto screen
- `get_display_count()` - Returns number of cryptos

**Display Format (per crypto):**
```
Row 0: HH:MM          +5.2%
Row 1: BTC:        $95432
```

**Configuration:**
```python
CRYPTO_MODULE_CONFIG = {
    'enabled': True,
    'symbols': {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'SOL': 'solana',
    },
    'fiat': 'usd',
    'update_interval': 600,  # 10 minutes
    'display_duration': 10,  # seconds per coin
    'timeout': 10,
    'lcd_max_size': 16
}
```

**API**: CoinGecko (no API key needed)  
**Update Frequency**: Every 10 minutes (configurable)

---

## 🛠️ Creating Custom Modules

### Step-by-Step Guide

#### Step 1: Create Module File

Create a new file in the `modules/` directory:

```bash
nano modules/example.py
```

#### Step 2: Import Base Module

```python
"""Stock module for displaying stock prices"""

import time
import requests
from datetime import datetime
from .base import BaseModule


class StockModule(BaseModule):
    """Module for displaying stock prices"""
    
    def __init__(self, lcd, config):
        super().__init__('Stock', lcd, config)
        self.symbols = config.get('symbols', ['AAPL', 'GOOGL'])
        self.api_key = config.get('api_key')
        self.timeout = config.get('timeout', 10)
        self.lcd_max_size = config.get('lcd_max_size', 16)
```

#### Step 3: Implement Required Methods

**1. fetch_data() - Get data from API or source:**

```python
def fetch_data(self):
    """Fetch stock prices from API"""
    try:
        # Example API call
        response = requests.get(
            'https://api.example.com/stocks',
            params={'symbols': ','.join(self.symbols)},
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Stock data fetched: {list(data.keys())}")
            return data
        else:
            return self._get_error_data()
    
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        return self._get_error_data()

def _get_error_data(self):
    """Return error data structure"""
    error_data = {}
    for symbol in self.symbols:
        error_data[symbol] = {
            'price': 'Error',
            'change': 0
        }
    return error_data
```

**2. display() - Show data on LCD:**

```python
def display(self):
    """Display stock information"""
    if not self.data:
        self.update_data()
    
    if not self.data:
        return
    
    # Display each stock
    for symbol in self.symbols:
        if symbol in self.data:
            self._display_stock(symbol, self.data[symbol])
            time.sleep(self.display_duration)

def _display_stock(self, symbol, data):
    """Display a single stock"""
    self.lcd.clear()
    
    # Display time
    now = datetime.now()
    self.lcd.cursor_pos = (0, 0)
    self.lcd.write_string(now.strftime("%H:%M"))
    
    # Display change percentage
    change = str(data['change'])
    self.lcd.cursor_pos = (0, self.lcd_max_size - len(change) - 1)
    self.lcd.write_string(f"{change}%")
    
    # Display symbol and price
    self.lcd.cursor_pos = (1, 0)
    self.lcd.write_string(f"{symbol}:")
    
    price = str(data['price'])
    self.lcd.cursor_pos = (1, self.lcd_max_size - len(price))
    self.lcd.write_string(price)
```

**3. Optional: Override other methods:**

```python
def get_display_count(self):
    """Return number of screens this module displays"""
    return len(self.symbols)

def fetch_data(self):
    """Fetch data from API"""
    # API clients handle caching internally
    # Pass update_interval as cache_duration for consistency
    return get_stock_prices(
        symbols=self.symbols,
        api_key=self.api_key,
        timeout=self.timeout,
        cache_duration=self.update_interval  # Pass to API client
    )
```

#### Step 4: Add Configuration

Edit `config.py`:

```python
# Stock Module Configuration
STOCK_MODULE_CONFIG = {
    'enabled': True,
    'symbols': ['AAPL', 'GOOGL', 'TSLA'],
    'api_key': os.getenv('STOCK_API_KEY'),
    'update_interval': 300,  # 5 minutes
    'display_duration': 10,
    'timeout': 10,
    'lcd_max_size': LCD_CONFIG['max_size']
}

# Add to module order
MODULE_ORDER = ['weather', 'crypto', 'stock']
```

#### Step 5: Register Module

Edit `main.py` to register your module:

```python
from modules.stock_module import StockModule

def initialize_modules(lcd, ip):
    """Initialize all enabled modules"""
    modules = {}
    
    # ... existing modules ...
    
    # Initialize Stock Module
    if STOCK_MODULE_CONFIG['enabled']:
        modules['stock'] = StockModule(lcd, STOCK_MODULE_CONFIG)
        print("Stock module initialized")
    
    return modules
```

Don't forget to import the config:

```python
from config import (
    LCD_CONFIG,
    WEATHER_MODULE_CONFIG,
    CRYPTO_MODULE_CONFIG,
    STOCK_MODULE_CONFIG,  # Add this
    APP_CONFIG,
    MODULE_ORDER
)
```

#### Step 6: Test Your Module

```bash
# Test manually first
python main.py

# Check logs for your module
# Should see: "Stock module initialized"
```

---

## 📋 Module Template

Here's a complete template for a new module:

```python
"""Custom module template"""

import time
import requests
from datetime import datetime
from .base import BaseModule


class CustomModule(BaseModule):
    """Module for displaying custom data"""
    
    def __init__(self, lcd, config):
        super().__init__('Custom', lcd, config)
        # Add your configuration here
        self.api_key = config.get('api_key')
        self.timeout = config.get('timeout', 10)
        self.lcd_max_size = config.get('lcd_max_size', 16)
    
    def fetch_data(self):
        """Fetch data from API or source"""
        try:
            # Your data fetching logic here
            response = requests.get(
                'https://api.example.com/endpoint',
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._get_error_data()
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            return self._get_error_data()
    
    def _get_error_data(self):
        """Return default error structure"""
        return {'error': True, 'message': 'Error'}
    
    def display(self):
        """Display data on LCD"""
        if not self.data:
            self.update_data()
        
        if not self.data:
            return
        
        # Your display logic here
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Custom Module")
        
        # Display your data on row 1
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(str(self.data.get('value', 'N/A')))
        
        time.sleep(self.display_duration)
    
    def get_display_count(self):
        """Return number of screens (optional)"""
        return 1  # Default is 1
```

---

## 🎯 Best Practices

### 1. Error Handling
Always wrap API calls in try-except blocks and provide fallback data:

```python
def fetch_data(self):
    try:
        response = requests.get(url, timeout=self.timeout)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return self._get_error_data()
```

### 2. LCD Display
Remember the 16x2 LCD constraints:
- Row 0: 16 characters
- Row 1: 16 characters
- Keep text short and readable

```python
# Good - fits in 16 chars
"BTC:     $95432"

# Bad - too long
"Bitcoin Price: $95432"
```

### 3. Update Intervals
Choose appropriate update frequencies:
- Fast updates (stocks): `update_interval = 60` (1 minute)
- Normal updates (crypto/weather): `update_interval = 600` (10 minutes)
- Slow updates (weather): `update_interval = 1800` (30 minutes)

### 4. Display Duration
Balance information density with readability:
- Simple data: `display_duration = 5` seconds
- Normal data: `display_duration = 10` seconds
- Complex data: `display_duration = 15` seconds

### 5. API Rate Limits
Respect API rate limits:
- Use appropriate `update_interval` (passed as `cache_duration` to API clients)
- All API clients use centralized caching via `cache_utils.py`
- Caching is automatic - no manual cache management needed
- Default cache duration: 600 seconds (10 minutes)

### 6. Configuration
Make everything configurable:
```python
def __init__(self, lcd, config):
    super().__init__('MyModule', lcd, config)
    self.param1 = config.get('param1', default_value)
    self.param2 = config.get('param2', default_value)
```

### 7. Logging
Print useful debug information:
```python
print(f"Module initialized")
print(f"Data fetched: {data}")
print(f"Error occurred: {error}")
```

---

## 🔍 Module Examples

### Simple Module (No API)

```python
class RandomNumberModule(BaseModule):
    """Display random numbers"""
    
    def fetch_data(self):
        import random
        return {'number': random.randint(1, 100)}
    
    def display(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Random Number")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(str(self.data['number']))
        time.sleep(self.display_duration)
```

### Multi-Screen Module

```python
class NewsModule(BaseModule):
    """Display multiple news headlines"""
    
    def display(self):
        headlines = self.data.get('headlines', [])
        
        for headline in headlines[:5]:  # Show first 5
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string("News:")
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(headline[:16])  # Truncate to 16 chars
            time.sleep(self.display_duration)
```

### Module with Custom Update Logic

```python
class CustomUpdateModule(BaseModule):
    """Module with conditional data fetching"""
    
    def fetch_data(self):
        # Only fetch during business hours
        now = datetime.now()
        if 9 <= now.hour <= 17:  # 9 AM to 5 PM
            return get_stock_data(
                cache_duration=self.update_interval
            )
        return None  # Skip fetching outside business hours
```

---

## 📊 Module Execution Flow

```
1. main.py starts
   └─> initialize_modules()
       └─> Creates instances of enabled modules

2. Main loop begins
   └─> For each module in MODULE_ORDER:
       ├─> module.update_data()
       │   └─> fetch_data()
       │       ├─> API client checks internal cache
       │       └─> Updates self.data (if valid)
       │
       └─> module.display()
           └─> Shows data on LCD
           └─> Sleeps for display_duration
```

---

## 🐛 Debugging

### Check Module Loading
```python
# In main.py
modules = initialize_modules(lcd, ip)
print(f"Loaded modules: {list(modules.keys())}")
```

### Check Data Fetching
```python
# In your module's fetch_data()
print(f"Fetched data: {data}")
```

### Check Display
```python
# In your module's display()
print(f"Displaying: {self.data}")
```

### Test Manually
```python
# Create a test script
from modules.my_module import MyModule
from config import MY_MODULE_CONFIG

# Mock LCD for testing
class MockLCD:
    def clear(self): pass
    def write_string(self, text): print(f"LCD: {text}")
    cursor_pos = (0, 0)

lcd = MockLCD()
module = MyModule(lcd, MY_MODULE_CONFIG)
module.update_data()
module.display()
```

---

## 📝 Module Checklist

Before deploying your module, ensure:

- [ ] Inherits from `BaseModule`
- [ ] Implements `fetch_data()` method
- [ ] Implements `display()` method
- [ ] Has error handling in `fetch_data()`
- [ ] Has `_get_error_data()` method
- [ ] Configuration added to `config.py`
- [ ] Registered in `main.py`
- [ ] Added to `MODULE_ORDER`
- [ ] LCD output fits in 16x2
- [ ] Respects API rate limits
- [ ] Logs useful debug info

---

## 🔗 Related Documentation

- [I2C_SETUP.md](I2C_SETUP.md) - Complete I2C setup and troubleshooting
- [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) - Detailed configuration options
- [SYSTEMD_SETUP.md](SYSTEMD_SETUP.md) - Service setup and management
- [FAQ.md](FAQ.md) - Frequently asked questions
- [README.md](../README.md) - Project overview and quick start

---

## 📚 Additional Resources

- Python `requests` library: https://requests.readthedocs.io/
- RPLCD documentation: https://rplcd.readthedocs.io/
- Python `datetime` module: https://docs.python.org/3/library/datetime.html
- Design Patterns: https://refactoring.guru/design-patterns

---

**Last Updated**: November 20, 2025

---

**Back to main README**: [README.md](../README.md)

