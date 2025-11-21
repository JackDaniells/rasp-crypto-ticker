"""Crypto module for displaying cryptocurrency prices"""

import time
from datetime import datetime
from .base import BaseModule
from clients import get_crypto_prices
from utils.lcd_wrapper import ROW_FIRST, ROW_SECOND, POS_RIGHT


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
        
        # Client returns None on failure
        data = get_crypto_prices(
            coingecko_ids=coingecko_ids,
            fiat_currency=self.fiat,
            timeout=self.timeout,
            cache_duration=self.update_interval
        )
        
        return data
    
    def display(self):
        """Display cryptocurrency information"""
        if not self.is_data_ready():
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
        
        # first row: time and 24h change percentage
        # Display time
        now = datetime.now()
        self.lcd.write_string(row=ROW_FIRST, text=now.strftime("%H:%M"))
        # Display 24h change percentage (use dummy value if missing)
        change_key = f'{self.fiat}_24h_change'
        variation = str(round(data.get(change_key, 0), 1))
        self.lcd.write_string(row=ROW_FIRST, text=f"{variation}%", pos=POS_RIGHT)
        
        # second row: crypto acronym and value
        # Display crypto acronym (e.g., 'BTC')
        self.lcd.write_string(row=ROW_SECOND, text=f"{acronym}:")
        # Display crypto value (use dummy value if missing)
        value = str(data.get(self.fiat, '--'))
        self.lcd.write_string(row=ROW_SECOND, text=f"${value}", pos=POS_RIGHT)
    
    def get_display_count(self):
        """Return number of screens this module displays"""
        return len(self.symbols)

