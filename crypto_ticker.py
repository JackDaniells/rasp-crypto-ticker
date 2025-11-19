"""Module providing a simple weather and crypto ticker"""

import time
from datetime import datetime
import requests
from RPLCD.i2c import CharLCD
import os

REQUESTS_TIMEOUT = 10

# lcd config
LCD_MAX_SIZE = 16

# crypto config
CONFIG_CRYPTO_FIAT = 'usd'

BTC_CRYPTO_SYMBOL = 'btc'
ETH_CRYPTO_SYMBOL = 'eth'
SOL_CRYPTO_SYMBOL = 'sol'

# weather config
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# global functions
def get_lcd_center_position(text):
    """return center position from text on screen"""
    position = round((LCD_MAX_SIZE-len(text))/2)
    position = max(position, 0)
    return position

# LCD functions
def lcd_write_string_centered(lcd, row, text):
    """write string on lcd row centered"""
    pos = get_lcd_center_position(text)
    lcd.cursor_pos = (row, pos)
    lcd.write_string(text)

def init_lcd(version):
    """start LCD 16x2 screen"""
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=LCD_MAX_SIZE, rows=2, dotsize=8)
    time.sleep(2)
    lcd.clear()
    lcd_write_string_centered(lcd, 0, "CRYPTO TICKER")
    lcd_write_string_centered(lcd, 1, version)
    time.sleep(10)
    return lcd

def establish_connection(lcd):
    """print connection status and return IP address"""
    lcd.clear()
    connected = False
    ip = 0
    while not connected:
        try:
            lcd_write_string_centered(lcd, 0, "Connecting...")
            res = requests.get("http://ipinfo.io/ip", timeout=REQUESTS_TIMEOUT)
            if res.status_code == 200:
                connected = True
                ip = res.text.strip()
                print(ip)
            else:
                print(res)
                lcd.clear()
                lcd_write_string_centered(lcd, 0, "Error when get IP")
                lcd_write_string_centered(lcd, 1, "Retrying...")
                time.sleep(5)
        except Exception as e:
            print(f"Connection error: {e}")
            lcd.clear()
            lcd_write_string_centered(lcd, 0, "Connection failed")
            lcd_write_string_centered(lcd, 1, "Retrying...")
            time.sleep(5)
    lcd.clear()
    lcd_write_string_centered(lcd, 0,"Connected!")
    lcd_write_string_centered(lcd, 1,f"IP:{ip}")
    time.sleep(5)
    return ip

def print_crypto_ticker(lcd, symbol, data):
    """print crypto ticker"""
    lcd.clear()
    now = datetime.now()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(now.strftime("%H:%M"))

    # crypto variation
    variation = str(round(data['usd_24h_change'], 1))
    lcd.cursor_pos = (0, LCD_MAX_SIZE-len(variation)-1)
    lcd.write_string(f"{variation}%")

    # crypto symbol
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"{symbol.upper()}:")

    # crypto value
    value = str(data[CONFIG_CRYPTO_FIAT])
    lcd.cursor_pos = (1, LCD_MAX_SIZE-len(value)-1)
    lcd.write_string(f"${value}")

def print_clock(lcd):
    """print crypto datetime clock"""
    lcd.clear()

    # date time
    lcd.cursor_pos = (0, 0)
    now = datetime.now()
    lcd.write_string(now.strftime("%d/%m/%Y %H:%M"))

def print_temperature(lcd, weather):
    """print temperature"""
    print_clock(lcd)
    text = f"Temp: {weather['current']['temp_c']}c"
    lcd_write_string_centered(lcd, 1, text)

def print_sensation(lcd, weather):
    """print termic sensation"""
    print_clock(lcd)
    text = f"Sens: {weather['current']['feelslike_c']}c"
    lcd_write_string_centered(lcd, 1, text)

def print_condition(lcd, weather):
    """print weather condition"""
    print_clock(lcd)
    text = weather['current']['condition']['text']
    lcd_write_string_centered(lcd, 1, text)

# API functions
def get_coin_prices():
    """get coin prices from coingecko API"""
    params = {
        'symbols': f'{BTC_CRYPTO_SYMBOL},{ETH_CRYPTO_SYMBOL},{SOL_CRYPTO_SYMBOL}',
        'vs_currencies': CONFIG_CRYPTO_FIAT,
        'include_24hr_change': 'true',
        'precision': '2'
    }
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price", params=params, timeout=REQUESTS_TIMEOUT)
        if res.status_code == 200:
            data = res.json()
        else:
            data = {
                'btc': {'usd': 'Error', 'usd_24h_change': 0}, 
                'eth': {'usd': 'Error', 'usd_24h_change': 0}, 
                'sol': {'usd': 'Error', 'usd_24h_change': 0},
                'sample': True
            }
    except Exception as e:
        print(f"Error fetching coin prices: {e}")
        data = {
            'btc': {'usd': 'Error', 'usd_24h_change': 0}, 
            'eth': {'usd': 'Error', 'usd_24h_change': 0}, 
            'sol': {'usd': 'Error', 'usd_24h_change': 0},
            'sample': True
        }
    print(f"coins: {data}")
    return data

def get_weather_info(ip):
    """get weather info from weatherapi"""
    params = {
        'q': ip,
        'key': WEATHER_API_KEY
    }
    try:
        res = requests.get("http://api.weatherapi.com/v1/current.json", params=params, timeout=REQUESTS_TIMEOUT)
        if res.status_code == 200:
            data = res.json()
        else:
            data = {
                "location": {
                    "name": "Error"
                },
                "current": {
                    "temp_c": 0,
                    "condition": {
                        "text": "Error"
                    },
                    "feelslike_c": 0
                },
                'sample': True
            }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        data = {
            "location": {
                "name": "Error"
            },
            "current": {
                "temp_c": 0,
                "condition": {
                    "text": "Error"
                },
                "feelslike_c": 0
            },
            'sample': True
        }
    print(f"weather: {data}")
    return data


# main function
def main():
    """main"""
    lcd = init_lcd("V1.1.0")
    ip = establish_connection(lcd)
    cryptos = {}
    weather = {}

    ticks = 0
    while True:
        try:
            # update prices and weather every 10 minutes
            if ticks % 10 == 0:
                cryptos = get_coin_prices()
                weather = get_weather_info(ip)

            ## update criptos if is empty or value is sampled
            if len(cryptos) == 0 or "sample" in cryptos:
                cryptos = get_coin_prices()

            if len(weather) == 0 or "sample" in weather:
                weather = get_weather_info(ip)

            print_temperature(lcd, weather)
            time.sleep(10)

            print_sensation(lcd, weather)
            time.sleep(10)

            print_condition(lcd, weather)
            time.sleep(10)

            print_crypto_ticker(lcd, BTC_CRYPTO_SYMBOL, cryptos[BTC_CRYPTO_SYMBOL])
            time.sleep(10)

            print_crypto_ticker(lcd, ETH_CRYPTO_SYMBOL, cryptos[ETH_CRYPTO_SYMBOL])
            time.sleep(10)

            print_crypto_ticker(lcd, SOL_CRYPTO_SYMBOL, cryptos[SOL_CRYPTO_SYMBOL])
            time.sleep(10)

            ticks += 1
        except Exception as e:
            print(f"Error in main loop: {e}")
            try:
                lcd.clear()
                lcd_write_string_centered(lcd, 0, "Display Error")
                lcd_write_string_centered(lcd, 1, "Recovering...")
            except Exception as lcd_error:
                print(f"LCD error: {lcd_error}")
            time.sleep(5)

# call main function
main()
