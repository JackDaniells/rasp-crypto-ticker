"""Modular Crypto Ticker - Main Application"""

import time
import requests
from RPLCD.i2c import CharLCD

from config import (
    LCD_CONFIG,
    WEATHER_MODULE_CONFIG,
    CRYPTO_MODULE_CONFIG,
    APP_CONFIG,
    MODULE_ORDER
)
from modules.weather_time import WeatherModule
from modules.crypto_module import CryptoModule


def lcd_write_string_centered(lcd, row, text, max_size=16):
    """Write string on LCD row centered"""
    position = max(round((max_size - len(text)) / 2), 0)
    lcd.cursor_pos = (row, position)
    lcd.write_string(text)


def init_lcd(version):
    """Initialize LCD 16x2 screen"""
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=LCD_CONFIG['address'],
        port=LCD_CONFIG['port'],
        cols=LCD_CONFIG['cols'],
        rows=LCD_CONFIG['rows'],
        dotsize=LCD_CONFIG['dotsize']
    )
    time.sleep(2)
    lcd.clear()
    lcd_write_string_centered(lcd, 0, "CRYPTO TICKER", LCD_CONFIG['max_size'])
    lcd_write_string_centered(lcd, 1, version, LCD_CONFIG['max_size'])
    time.sleep(10)
    return lcd


def establish_connection(lcd):
    """Establish internet connection and return IP address"""
    lcd.clear()
    connected = False
    ip = None
    
    while not connected:
        try:
            lcd_write_string_centered(lcd, 0, "Connecting...", LCD_CONFIG['max_size'])
            res = requests.get(
                "http://ipinfo.io/ip",
                timeout=APP_CONFIG['connection_timeout']
            )
            if res.status_code == 200:
                connected = True
                ip = res.text.strip()
                print(f"Connected! IP: {ip}")
            else:
                print(f"Connection error: {res.status_code}")
                lcd.clear()
                lcd_write_string_centered(lcd, 0, "Error when get IP", LCD_CONFIG['max_size'])
                lcd_write_string_centered(lcd, 1, "Retrying...", LCD_CONFIG['max_size'])
                time.sleep(APP_CONFIG['retry_delay'])
        except Exception as e:
            print(f"Connection error: {e}")
            lcd.clear()
            lcd_write_string_centered(lcd, 0, "Connection failed", LCD_CONFIG['max_size'])
            lcd_write_string_centered(lcd, 1, "Retrying...", LCD_CONFIG['max_size'])
            time.sleep(APP_CONFIG['retry_delay'])
    
    lcd.clear()
    lcd_write_string_centered(lcd, 0, "Connected!", LCD_CONFIG['max_size'])
    lcd_write_string_centered(lcd, 1, f"IP:{ip}", LCD_CONFIG['max_size'])
    time.sleep(5)
    return ip


def initialize_modules(lcd, ip):
    """Initialize all enabled modules"""
    modules = {}
    
    # Initialize Weather & Time Module
    if WEATHER_MODULE_CONFIG['enabled']:
        weather_config = WEATHER_MODULE_CONFIG.copy()
        weather_config['ip'] = ip
        modules['weather'] = WeatherModule(lcd, weather_config)
        print("Weather & Time module initialized")
    
    # Initialize Crypto Module
    if CRYPTO_MODULE_CONFIG['enabled']:
        modules['crypto'] = CryptoModule(lcd, CRYPTO_MODULE_CONFIG)
        print("Crypto module initialized")
    
    return modules


def display_module_status(lcd, modules):
    """Display which modules are active"""
    lcd.clear()
    enabled_modules = [name.capitalize() for name in modules.keys()]
    
    if enabled_modules:
        modules_text = ", ".join(enabled_modules)
        lcd_write_string_centered(lcd, 0, "Active Modules:", LCD_CONFIG['max_size'])
        
        # If text is too long, scroll or truncate
        if len(modules_text) > LCD_CONFIG['max_size']:
            lcd.cursor_pos = (1, 0)
            lcd.write_string(modules_text[:LCD_CONFIG['max_size']])
        else:
            lcd_write_string_centered(lcd, 1, modules_text, LCD_CONFIG['max_size'])
    else:
        lcd_write_string_centered(lcd, 0, "No modules", LCD_CONFIG['max_size'])
        lcd_write_string_centered(lcd, 1, "enabled!", LCD_CONFIG['max_size'])
    
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
    
    # Display active modules
    display_module_status(lcd, modules)
    
    if not modules:
        lcd.clear()
        lcd_write_string_centered(lcd, 0, "No modules", LCD_CONFIG['max_size'])
        lcd_write_string_centered(lcd, 1, "enabled!", LCD_CONFIG['max_size'])
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
            lcd_write_string_centered(lcd, 0, "Goodbye!", LCD_CONFIG['max_size'])
            time.sleep(2)
            lcd.clear()
            break
        
        except Exception as e:
            print(f"Error in main loop: {e}")
            try:
                lcd.clear()
                lcd_write_string_centered(lcd, 0, "Display Error", LCD_CONFIG['max_size'])
                lcd_write_string_centered(lcd, 1, "Recovering...", LCD_CONFIG['max_size'])
            except Exception as lcd_error:
                print(f"LCD error: {lcd_error}")
            time.sleep(5)


if __name__ == "__main__":
    main()

