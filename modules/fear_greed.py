"""
Fear and Greed Index Module

Displays the cryptocurrency Fear and Greed Index from Alternative.me
Index ranges from 0 (Extreme Fear) to 100 (Extreme Greed)
"""

import time
from datetime import datetime
from modules.base import BaseModule
from clients import get_fear_greed_index


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
        title_pos = (16 - len(title)) // 2
        self.lcd.cursor_pos = (0, title_pos)
        self.lcd.write_string(title)
        
        # Line 2: Value and classification
        self.lcd.cursor_pos = (1, 0)
        display_text = f"{index_value} - {classification}"
        
        # Center the text
        text_pos = max(0, (16 - len(display_text)) // 2)
        self.lcd.cursor_pos = (1, text_pos)
        self.lcd.write_string(display_text[:16])
        
        time.sleep(self.display_duration)

