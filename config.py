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
    'display_duration': 5,
    'timeout': 10,
    'lcd_max_size': LCD_CONFIG['max_size'],
    'max_failed_attempts': 3
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
    'lcd_max_size': LCD_CONFIG['max_size'],
    'max_failed_attempts': 3
}

# ============================================================================
# FEAR & GREED INDEX MODULE CONFIGURATION
# ============================================================================
FEAR_GREED_MODULE_CONFIG = {
    'enabled': True,
    'update_interval': 3600,  # 1 hour (index updates every 8 hours)
    'display_duration': 5,   # seconds
    'timeout': 10,
    'max_failed_attempts': 3
}

# ============================================================================
# MARKET CAP MODULE CONFIGURATION
# ============================================================================
MARKET_CAP_MODULE_CONFIG = {
    'enabled': True,
    'fiat': 'usd',
    'update_interval': 600,   # 10 minutes
    'display_duration': 5,   # seconds
    'timeout': 10,
    'max_failed_attempts': 3
}

# ============================================================================
# ALTCOIN SEASON MODULE CONFIGURATION
# ============================================================================
# Displays Altcoin Season Index: % of top 100 coins outperforming BTC over 7d and 30d
# Calculated using CoinGecko API (free, no API key required)
# Shows 2 screens: Screen 1 (7d), Screen 2 (30d) with percentage + season classification
# Season indicators: 75%+ = Alt Season, 25%- = BTC Season, 25-75% = Mixed
ALT_SEASON_MODULE_CONFIG = {
    'enabled': True,
    'update_interval': 600,   # 10 minutes
    'display_duration': 5,   # seconds
    'timeout': 10,
    'max_failed_attempts': 3
}

# ============================================================================
# BTC DOMINANCE MODULE CONFIGURATION
# ============================================================================
# Displays Bitcoin Dominance: % of total crypto market cap that is Bitcoin
# Fetched from CoinGecko Global API (free, no API key required)
# Higher dominance (>50%) = BTC Season, Lower (<40%) = Alt-friendly environment
BTC_DOMINANCE_MODULE_CONFIG = {
    'enabled': True,
    'update_interval': 600,   # 10 minutes
    'display_duration': 5,   # seconds
    'timeout': 10,
    'max_failed_attempts': 3
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
MODULE_ORDER = ['weather', 'fear_greed', 'btc_dominance', 'alt_season', 'market_cap'] + ['crypto'] * 3

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
