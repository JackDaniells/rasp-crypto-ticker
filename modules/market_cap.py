"""
Crypto Market Cap Module

Displays total cryptocurrency market capitalization from CoinGecko
Shows total market cap and 24h change percentage
"""

import time
from datetime import datetime
from modules.base import BaseModule
from clients import get_global_data
from utils import format_large_number


class MarketCapModule(BaseModule):
    """Module for displaying total crypto market cap"""
    
    def __init__(self, lcd, config):
        """Initialize Market Cap module"""
        super().__init__("Market Cap", lcd, config)
        
        # Validate required config keys
        required_keys = ['update_interval', 'display_duration', 'timeout', 'fiat', 'max_failed_attempts']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(
                f"Market Cap module missing required config keys: {', '.join(missing_keys)}. "
                "Check config.py"
            )
        
        self.timeout = config['timeout']
        self.fiat = config['fiat'].lower()
        
    def fetch_data(self):
        """Fetch global market cap data"""
        return get_global_data(timeout=self.timeout, cache_duration=self.update_interval)
    
    def _format_market_cap(self, value):
        """Format market cap value to readable string (e.g., 1.2T, 450B)"""
        return format_large_number(value)
    
    def display(self):
        """Display market cap on LCD"""
        if not self.is_data_ready():
            return
        
        # Get market cap and change percentage
        total_market_cap = self.data.get('total_market_cap', {}).get(self.fiat, '--')
        change_24h = self.data.get('market_cap_change_percentage_24h_usd', '--')
        
        # Format values
        market_cap_str = self._format_market_cap(total_market_cap)
        
        if change_24h != '--':
            try:
                change_str = f"{float(change_24h):+.1f}%"
            except (ValueError, TypeError):
                change_str = '--'
        else:
            change_str = '--'
        
        # Display Market Cap
        self.lcd.clear()
        
        # Line 1: Time and 24h change
        now = datetime.now()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(now.strftime("%H:%M"))
        
        # Right-align 24h change
        self.lcd.cursor_pos = (0, 16 - len(change_str))
        self.lcd.write_string(change_str)
        
        # Line 2: Market cap label (left) and value (right)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Mkt. Cap:")
        
        # Right-align market cap value
        value_text = f"${market_cap_str}"
        self.lcd.cursor_pos = (1, 16 - len(value_text))
        self.lcd.write_string(value_text)
        
        time.sleep(self.display_duration)

