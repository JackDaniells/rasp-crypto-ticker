"""Weather and Time module for displaying weather information and clock"""

import time
from datetime import datetime
from .base import BaseModule
from clients import get_weather


class WeatherModule(BaseModule):
    """Module for displaying weather and time information"""
    
    def __init__(self, lcd, config):
        super().__init__('Weather', lcd, config)
        
        # Validate required configuration
        required_keys = ['api_key', 'ip', 'timeout', 'lcd_max_size']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Weather module missing required config keys: {', '.join(missing_keys)}. Check config.py")
        
        self.api_key = config['api_key']
        self.ip = config['ip']
        self.timeout = config['timeout']
        self.lcd_max_size = config['lcd_max_size']
    
    def fetch_data(self):
        """Fetch weather data from weatherapi"""

        data = get_weather(
            api_key=self.api_key,
            location=self.ip,
            timeout=self.timeout
        )
        
        return data
    
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
        if not self.is_data_ready():
            return
        
        # Use dummy values if data fields are missing
        temp_c = self.data.get('current', {}).get('temp_c', '--')
        feelslike_c = self.data.get('current', {}).get('feelslike_c', '--')
        condition = self.data.get('current', {}).get('condition', {}).get('text', '--')
        
        # Screen 1: Temperature
        self.lcd.clear()
        self._print_clock()
        text = f"Temp: {temp_c}c"
        self._lcd_write_string_centered(1, text)
        time.sleep(self.display_duration)
        
        # Screen 2: Feels like
        self.lcd.clear()
        self._print_clock()
        text = f"Sens: {feelslike_c}c"
        self._lcd_write_string_centered(1, text)
        time.sleep(self.display_duration)
        
        # Screen 3: Condition
        self.lcd.clear()
        self._print_clock()
        self._lcd_write_string_centered(1, condition)
        time.sleep(self.display_duration)
    
    def get_display_count(self):
        """Return number of screens this module displays"""
        return 3

