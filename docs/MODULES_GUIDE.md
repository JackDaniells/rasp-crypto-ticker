# Module Development Guide

Complete guide for understanding and creating modules for the Raspberry Pi Crypto Ticker.

---

## 📦 Existing Modules

### Weather & Time Module

**File**: `modules/weather_time.py` (107 lines)

**Features:**
- 3 display screens: Temperature, Feels Like, Weather Condition
- Auto-fetches weather based on IP location
- Shows current time on each screen
- Centered text display

**Methods:**
- `fetch_data()` - Fetches weather from WeatherAPI
- `display()` - Shows 3 screens (temp, sensation, condition)
- `_print_clock()` - Displays date/time on row 0
- `_lcd_write_string_centered()` - Centers text on LCD

**Display Screens:**
1. Temperature (°C) with time on top
2. Feels Like temperature (°C) with time on top
3. Weather condition (e.g., "Sunny", "Cloudy") with time on top

**Configuration:**
```python
WEATHER_MODULE_CONFIG = {
    'enabled': True,
    'api_key': os.getenv('WEATHER_API_KEY'),
    'update_interval': 600,  # 10 minutes
    'display_duration': 10,  # seconds per screen
    'timeout': 10,
    'lcd_max_size': 16
}
```

**API:** WeatherAPI (requires API key)  
**Update Frequency:** Every 10 minutes (configurable)

---

### Crypto Module

**File**: `modules/crypto_module.py` (99 lines)

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

**API:** CoinGecko (no API key needed)  
**Update Frequency:** Every 10 minutes (configurable)

---

### Base Module

**File**: `modules/base_module.py` (57 lines)

The abstract base class that all modules inherit from.

**Key Features:**
- Abstract methods: `fetch_data()` and `display()`
- Automatic update interval management
- Enable/disable functionality
- Display duration control

**Methods:**
- `should_update_data()` - Checks if data needs refreshing
- `update_data()` - Fetches and updates module data
- `is_enabled()` - Returns module enabled status
- `get_display_count()` - Returns number of screens

**Properties:**
- `self.name` - Module name
- `self.lcd` - LCD object
- `self.config` - Configuration dictionary
- `self.enabled` - Enabled status
- `self.display_duration` - Seconds per screen
- `self.update_interval` - Seconds between updates
- `self.data` - Cached data
- `self.last_update` - Timestamp of last update

---

## 🔄 Module Inheritance Hierarchy

```
        BaseModule (Abstract)
                │
        ┌───────┴───────┐
        │               │
WeatherModule     CryptoModule
        │               │
    3 screens       N screens
```

All custom modules should inherit from `BaseModule`.

---

## 🛠️ Creating a Custom Module

### Step 1: Create Module File

Create a new file in the `modules/` directory:

```bash
nano modules/stock_module.py
```

### Step 2: Import Base Module

```python
"""Stock module for displaying stock prices"""

import time
import requests
from datetime import datetime
from .base_module import BaseModule


class StockModule(BaseModule):
    """Module for displaying stock prices"""
    
    def __init__(self, lcd, config):
        super().__init__('Stock', lcd, config)
        self.symbols = config.get('symbols', ['AAPL', 'GOOGL'])
        self.api_key = config.get('api_key')
        self.timeout = config.get('timeout', 10)
        self.lcd_max_size = config.get('lcd_max_size', 16)
```

### Step 3: Implement Required Methods

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

def should_update_data(self):
    """Custom update logic (optional)"""
    # Use default from base class, or implement custom logic
    return super().should_update_data()
```

### Step 4: Add Configuration

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

### Step 5: Register Module

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

### Step 6: Test Your Module

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
from .base_module import BaseModule


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
- Use appropriate `update_interval`
- Cache data when possible
- Handle rate limit errors gracefully

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
    """Module with custom update timing"""
    
    def should_update_data(self):
        # Update only during business hours
        now = datetime.now()
        if 9 <= now.hour <= 17:  # 9 AM to 5 PM
            return super().should_update_data()
        return False
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
       │   └─> if should_update_data():
       │       └─> fetch_data()
       │           └─> Updates self.data
       │
       └─> module.display()
           └─> Shows data on LCD
           └─> Sleeps for display_duration
```

---

## 🐛 Debugging Modules

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
- [ ] Tested manually
- [ ] LCD output fits in 16x2
- [ ] Respects API rate limits
- [ ] Logs useful debug info
- [ ] Documentation written

---

## 🔗 Related Files

- `modules/base_module.py` - Base class implementation
- `modules/weather_time.py` - Example module with API and time display
- `modules/crypto_module.py` - Example module with multiple displays
- `config.py` - Configuration file
- `main.py` - Module registration

---

## 📚 Additional Resources

- Python `requests` library: https://requests.readthedocs.io/
- RPLCD documentation: https://rplcd.readthedocs.io/
- Python `datetime` module: https://docs.python.org/3/library/datetime.html

---

**Back to main README**: See [README.md](../README.md) for project overview and setup.

