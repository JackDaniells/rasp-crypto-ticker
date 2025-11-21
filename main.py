"""Modular Crypto Ticker - Main Application"""

import time
from RPLCD.i2c import CharLCD
from utils.lcd import SafeLCD, POS_CENTER, ROW_FIRST, ROW_SECOND

from config import (
    LCD_CONFIG,
    WEATHER_MODULE_CONFIG,
    CRYPTO_MODULE_CONFIG,
    FEAR_GREED_MODULE_CONFIG,
    MARKET_CAP_MODULE_CONFIG,
    ALT_SEASON_MODULE_CONFIG,
    BTC_DOMINANCE_MODULE_CONFIG,
    APP_CONFIG,
    MODULE_ORDER
)
from modules.weather_time import WeatherTimeModule
from modules.crypto_ticker import CryptoTickerModule
from modules.fear_greed import FearGreedModule
from modules.market_cap import MarketCapModule
from modules.alt_season import AltSeasonModule
from modules.btc_dominance import BTCDominanceModule
from clients import get_ip_address


def init_lcd(version):
    """Initialize LCD 16x2 screen with SafeLCD wrapper"""
    raw_lcd = CharLCD(
        i2c_expander='PCF8574',
        address=LCD_CONFIG['address'],
        port=LCD_CONFIG['port'],
        cols=LCD_CONFIG['cols'],
        rows=LCD_CONFIG['rows'],
        dotsize=LCD_CONFIG['dotsize']
    )
    
    # Wrap LCD with SafeLCD for automatic text validation
    lcd = SafeLCD(raw_lcd, max_size=LCD_CONFIG['max_size'])
    
    time.sleep(2)
    lcd.clear()
    lcd.write_string(row=ROW_FIRST, text="CRYPTO TICKER", pos=POS_CENTER)
    lcd.write_string(row=ROW_SECOND, text=version, pos=POS_CENTER)
    time.sleep(10)
    return lcd


def fetch_ip_address():
    """Attempt to get IP address from ipify API
    
    Returns:
        str: IP address if successful, None otherwise
    """
    return get_ip_address(timeout=APP_CONFIG['connection_timeout'])


def establish_connection(lcd):
    """Establish internet connection and return IP address"""
    lcd.clear()
    ip = None
    
    while ip is None:
        lcd.write_string(row=ROW_FIRST, text="Connecting...", pos=POS_CENTER)
        ip = fetch_ip_address()
        
        if ip is None:
            lcd.clear()
            lcd.write_string(row=ROW_FIRST, text="Conn. error", pos=POS_CENTER)
            lcd.write_string(row=ROW_SECOND, text="Retrying...", pos=POS_CENTER)
            time.sleep(APP_CONFIG['retry_delay'])
        else:
            print(f"Connected! IP: {ip}")
    
    lcd.clear()
    lcd.write_string(row=ROW_FIRST, text="Connected!", pos=POS_CENTER)
    lcd.write_string(row=ROW_SECOND, text=f"IP:{ip}", pos=POS_CENTER)
    time.sleep(2)
    return ip


def initialize_modules(lcd, ip):
    """Initialize all enabled modules"""
    modules = {}
    
    # Initialize Weather & Time Module
    if WEATHER_MODULE_CONFIG['enabled']:
        weather_config = WEATHER_MODULE_CONFIG.copy()
        weather_config['ip'] = ip
        modules['weather'] = WeatherTimeModule(lcd, weather_config)
        print("Weather & Time module initialized")
    
    # Initialize Crypto Module
    if CRYPTO_MODULE_CONFIG['enabled']:
        modules['crypto'] = CryptoTickerModule(lcd, CRYPTO_MODULE_CONFIG)
        print("Crypto module initialized")
    
    # Initialize Fear & Greed Index Module
    if FEAR_GREED_MODULE_CONFIG['enabled']:
        modules['fear_greed'] = FearGreedModule(lcd, FEAR_GREED_MODULE_CONFIG)
        print("Fear & Greed Index module initialized")
    
    # Initialize Market Cap Module
    if MARKET_CAP_MODULE_CONFIG['enabled']:
        modules['market_cap'] = MarketCapModule(lcd, MARKET_CAP_MODULE_CONFIG)
        print("Market Cap module initialized")
    
    # Initialize Bitcoin Dominance Module
    if BTC_DOMINANCE_MODULE_CONFIG['enabled']:
        modules['btc_dominance'] = BTCDominanceModule(lcd, BTC_DOMINANCE_MODULE_CONFIG)
        print("BTC Dominance module initialized")
    
    # Initialize Altcoin Season Module
    if ALT_SEASON_MODULE_CONFIG['enabled']:
        modules['alt_season'] = AltSeasonModule(lcd, ALT_SEASON_MODULE_CONFIG)
        print("Altcoin Season module initialized")
    
    return modules


def display_module_error(lcd):
    """Display error message when no modules are active"""
    lcd.clear()
    lcd.write_string(row=ROW_FIRST, text="No modules", pos=POS_CENTER)
    lcd.write_string(row=ROW_SECOND, text="enabled!", pos=POS_CENTER)
    time.sleep(5)


def main():
    """Main application loop"""
    print("Starting Crypto Ticker...")
    
    # Initialize LCD
    lcd = init_lcd(APP_CONFIG['version'])
    
    # Establish connection
    ip = establish_connection(lcd)
    
    # Initialize modules
    modules = initialize_modules(lcd, ip)
    
    if not modules:
        display_module_error(lcd)
        print("No modules enabled. Check config.py")
        return
    
    print("Starting main loop...")
    
    # Main loop
    while True:
        try:
            # Update and display modules in configured order
            for module_name in MODULE_ORDER:
                if module_name in modules:
                    module = modules[module_name]
                    
                    # Update module data if needed
                    module.update_data()
                    
                    # Display module
                    module.display()
        
        except KeyboardInterrupt:
            print("\nShutting down...")
            lcd.clear()
            lcd.write_string(row=ROW_FIRST, text="Goodbye!", pos=POS_CENTER)
            time.sleep(2)
            lcd.clear()
            break
        
        except Exception as e:
            print(f"Error in main loop: {e}")
            try:
                lcd.clear()
                lcd.write_string(row=ROW_FIRST, text="Display Error", pos=POS_CENTER)
                lcd.write_string(row=ROW_SECOND, text="Recovering...", pos=POS_CENTER)
            except Exception as lcd_error:
                print(f"LCD error: {lcd_error}")
            time.sleep(5)


if __name__ == "__main__":
    main()

