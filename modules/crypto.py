"""Crypto module for displaying cryptocurrency prices"""

import time
import requests
from datetime import datetime
from .base import BaseModule


class CryptoModule(BaseModule):
    """Module for displaying cryptocurrency prices"""
    
    def __init__(self, lcd, config):
        super().__init__('Crypto', lcd, config)
        
        # Validate required configuration
        required_keys = ['symbols', 'fiat', 'timeout', 'lcd_max_size']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Crypto module missing required config keys: {', '.join(missing_keys)}. Check config.py")
        
        self.symbols = config['symbols']
        self.fiat = config['fiat']
        self.timeout = config['timeout']
        self.lcd_max_size = config['lcd_max_size']
    
    def fetch_data(self):
        """Fetch cryptocurrency prices from CoinGecko API"""
        # Get CoinGecko IDs from the dict values
        coingecko_ids = ','.join(self.symbols.values())
        params = {
            'ids': coingecko_ids,
            'vs_currencies': self.fiat,
            'include_24hr_change': 'true',
            'precision': '2'
        }
        
        try:
            res = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params=params,
                timeout=self.timeout
            )
            if res.status_code == 200:
                data = res.json()
                print(f"Crypto data fetched: {list(data.keys())}")
                return data
            else:
                print(f"Crypto API error: {res.status_code}")
                return self._get_error_data()
        except Exception as e:
            print(f"Error fetching crypto prices: {e}")
            return self._get_error_data()
    
    def _get_error_data(self):
        """Return error data structure"""
        error_data = {}
        # Use CoinGecko IDs (dict values) for error data structure
        for coingecko_id in self.symbols.values():
            error_data[coingecko_id] = {
                self.fiat: 'Error',
                f'{self.fiat}_24h_change': 0
            }
        return error_data
    
    def display(self):
        """Display cryptocurrency information"""
        if not self.data:
            self.update_data()
        
        if not self.data:
            return
        
        # Display each crypto for configured duration
        # Iterate through acronyms and CoinGecko IDs
        for acronym, coingecko_id in self.symbols.items():
            if coingecko_id in self.data:
                self._display_crypto(acronym, self.data[coingecko_id])
                time.sleep(self.display_duration)
    
    def _display_crypto(self, acronym, data):
        """Display a single cryptocurrency"""
        self.lcd.clear()
        
        # Display time
        now = datetime.now()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(now.strftime("%H:%M"))
        
        # Display 24h change percentage
        change_key = f'{self.fiat}_24h_change'
        if change_key in data:
            variation = str(round(data[change_key], 1))
            self.lcd.cursor_pos = (0, self.lcd_max_size - len(variation) - 1)
            self.lcd.write_string(f"{variation}%")
        
        # Display crypto acronym (e.g., 'BTC')
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"{acronym}:")
        
        # Display crypto value
        value = str(data[self.fiat])
        self.lcd.cursor_pos = (1, self.lcd_max_size - len(value) - 1)
        self.lcd.write_string(f"${value}")
    
    def get_display_count(self):
        """Return number of screens this module displays"""
        return len(self.symbols)

