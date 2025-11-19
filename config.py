"""
Configuration file for the Raspberry Pi Crypto Ticker

All settings are managed here. For detailed configuration guide,
see docs/CONFIGURATION_GUIDE.md
"""

import os

# ============================================================================
# LCD HARDWARE CONFIGURATION
# ============================================================================
LCD_CONFIG = {
    'address': 0x27,
    'port': 1,
    'cols': 16,
    'rows': 2,
    'dotsize': 8,
    'max_size': 16
}

# ============================================================================
# WEATHER & TIME MODULE CONFIGURATION
# ============================================================================
WEATHER_MODULE_CONFIG = {
    'enabled': True,
    'api_key': os.getenv('WEATHER_API_KEY'),
    'update_interval': 600,
    'display_duration': 10,
    'timeout': 10,
    'lcd_max_size': LCD_CONFIG['max_size']
}

# ============================================================================
# CRYPTO MODULE CONFIGURATION
# ============================================================================
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

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================
APP_CONFIG = {
    'version': 'V2.0.0',
    'connection_timeout': 10,
    'retry_delay': 5
}

# ============================================================================
# MODULE DISPLAY ORDER
# ============================================================================
MODULE_ORDER = ['weather', 'crypto']

# ============================================================================
# QUICK REFERENCE
# ============================================================================
# Enable/disable modules:     Set 'enabled' to True or False
# Add cryptocurrencies:        Add to 'symbols': 'ACRONYM': 'coingecko-id'
# Change display time:         Modify 'display_duration' (seconds)
# Change update frequency:     Modify 'update_interval' (seconds)
# Reorder modules:             Modify MODULE_ORDER list
# 
# 📖 For complete configuration guide: see docs/CONFIGURATION_GUIDE.md
# ============================================================================
