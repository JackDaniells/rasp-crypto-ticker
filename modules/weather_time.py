"""Weather and Time module for displaying weather information and clock"""

import time
import requests
from datetime import datetime
from .base_module import BaseModule


class WeatherModule(BaseModule):
    """Module for displaying weather and time information"""
    
    def __init__(self, lcd, config):
        super().__init__('Weather', lcd, config)
        self.api_key = config.get('api_key')
        self.ip = config.get('ip')
        self.timeout = config.get('timeout', 10)
        self.lcd_max_size = config.get('lcd_max_size', 16)
    
    def fetch_data(self):
        """Fetch weather data from weatherapi"""
        if not self.api_key:
            print("Weather API key not configured")
            return self._get_error_data()
        
        params = {
            'q': self.ip,
            'key': self.api_key
        }
        
        try:
            res = requests.get(
                "http://api.weatherapi.com/v1/current.json",
                params=params,
                timeout=self.timeout
            )
            if res.status_code == 200:
                data = res.json()
                print(f"Weather data fetched: {data['location']['name']}")
                return data
            else:
                print(f"Weather API error: {res.status_code}")
                return self._get_error_data()
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_error_data()
    
    def _get_error_data(self):
        """Return error data structure"""
        return {
            "location": {
                "name": "Error"
            },
            "current": {
                "temp_c": 0,
                "condition": {
                    "text": "Error"
                },
                "feelslike_c": 0
            }
        }
    
    def _lcd_write_string_centered(self, row, text):
        """Write string on LCD row centered"""
        position = max(round((self.lcd_max_size - len(text)) / 2), 0)
        self.lcd.cursor_pos = (row, position)
        self.lcd.write_string(text)
    
    def _print_clock(self):
        """Print date and time on first row"""
        self.lcd.cursor_pos = (0, 0)
        now = datetime.now()
        self.lcd.write_string(now.strftime("%d/%m/%Y %H:%M"))
    
    def display(self):
        """Display weather and time information across multiple screens"""
        if not self.data:
            self.update_data()
        
        if not self.data:
            return
        
        # Screen 1: Temperature
        self.lcd.clear()
        self._print_clock()
        text = f"Temp: {self.data['current']['temp_c']}c"
        self._lcd_write_string_centered(1, text)
        time.sleep(self.display_duration)
        
        # Screen 2: Feels like
        self.lcd.clear()
        self._print_clock()
        text = f"Sens: {self.data['current']['feelslike_c']}c"
        self._lcd_write_string_centered(1, text)
        time.sleep(self.display_duration)
        
        # Screen 3: Condition
        self.lcd.clear()
        self._print_clock()
        text = self.data['current']['condition']['text']
        self._lcd_write_string_centered(1, text)
        time.sleep(self.display_duration)
    
    def get_display_count(self):
        """Return number of screens this module displays"""
        return 3


