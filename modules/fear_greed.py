"""
Fear and Greed Index Module

Displays the cryptocurrency Fear and Greed Index from Alternative.me
Index ranges from 0 (Extreme Fear) to 100 (Extreme Greed)
"""

import time
from datetime import datetime
from modules.base import BaseModule
from clients import get_fear_greed_index
from utils.lcd_wrapper import POS_CENTER, ROW_FIRST, ROW_SECOND


class FearGreedModule(BaseModule):
    """Module for displaying Fear and Greed Index"""
    
    def __init__(self, lcd, config):
        """Initialize Fear and Greed module"""
        super().__init__("Fear & Greed", lcd, config)
        
        # Validate required config keys
        required_keys = ['update_interval', 'display_duration', 'timeout', 'max_failed_attempts']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(
                f"Fear & Greed module missing required config keys: {', '.join(missing_keys)}. "
                "Check config.py"
            )
        
        self.timeout = config['timeout']
        
    def fetch_data(self):
        """Fetch Fear and Greed Index data"""
        return get_fear_greed_index(timeout=self.timeout, cache_duration=self.update_interval)
    
    def _shorten_classification(self, classification):
        """Shorten two-word classifications (e.g., 'Extreme Fear' -> 'Extr. Fear')"""
        if classification == '--':
            return classification
        
        words = classification.split()
        if len(words) == 2 and len(words[0]) > 4:
            words[0] = words[0][:4] + '.'
        
        return ' '.join(words)
    
    def display(self):
        """Display Fear and Greed Index on LCD"""
        if not self.is_data_ready():
            return
        
        # Get index value and classification
        index_value = self.data.get('value', '--')
        classification = self._shorten_classification(self.data.get('value_classification', '--'))
        
        # Display Fear & Greed Index
        self.lcd.clear()
        
        # Align center "Fear&Greed Idx." on first line
        title = "Fear&Greed Idx"
        self.lcd.write_string(row=ROW_FIRST, text=title, pos=POS_CENTER)
        
        # Line 2: Value and classification
        display_text = f"{index_value} - {classification}"
        self.lcd.write_string(row=ROW_SECOND, text=display_text, pos=POS_CENTER)
        
        time.sleep(self.display_duration)

