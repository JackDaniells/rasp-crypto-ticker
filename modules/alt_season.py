"""
Altcoin Season Module

Displays the Altcoin Season Index which shows what percentage of the top 100 
coins performed better than Bitcoin over the last 7 days and 30 days.

Calculated using CoinGecko API data (free, no API key required).
Shows two separate screens: one for 7d metric, one for 30d metric.

The season is determined by:
- 75% or more = Altcoin Season
- 25% or less = Bitcoin Season
- Between 25-75% = Mixed
"""

import time
from datetime import datetime
from modules.base import BaseModule
from clients import get_altcoin_season_index


class AltSeasonModule(BaseModule):
    """Module for displaying Altcoin Season Index"""
    
    def __init__(self, lcd, config):
        """Initialize Altcoin Season module"""
        super().__init__("Altcoin Season", lcd, config)
        
        # Validate required config keys
        required_keys = ['update_interval', 'display_duration', 'timeout', 'max_failed_attempts']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(
                f"Altcoin Season module missing required config keys: {', '.join(missing_keys)}. "
                "Check config.py"
            )
        
        self.timeout = config['timeout']
        
    def fetch_data(self):
        """Fetch Altcoin Season Index data"""
        return get_altcoin_season_index(timeout=self.timeout)
    
    def _get_season(self, index_value):
        """
        Determine market season based on Altcoin Season Index
        
        Args:
            index_value: Percentage of top 100 coins that outperformed Bitcoin (0-100)
        
        Returns:
            str: Season indicator
        """
        if index_value >= 75:
            return "Alt Season"
        elif index_value <= 25:
            return "BTC Season"
        else:
            return "Mixed"
    
    def display(self):
        """
        Display Altcoin Season Index on LCD
        Shows 2 screens (7d and 30d)
        """
        if not self.is_data_ready():
            return
        
        # Get altcoin season index values for both timeframes
        index_7d = self.data.get('value_7d')
        index_30d = self.data.get('value_30d')
        
        # Screen 1: 7-day Altcoin Season Index
        if index_7d is not None:
            self._display_screen(index_7d, '7d')
        
        # Screen 2: 30-day Altcoin Season Index
        if index_30d is not None:
            self._display_screen(index_30d, '30d')
    
    def _display_screen(self, index_value, timeframe):
        """Display a single Altcoin Season screen
        
        Args:
            index_value: The percentage value (0-100)
        """
        try:
            value_str = f"{int(index_value)}%"
            season = self._get_season(int(index_value))
        except (ValueError, TypeError):
            value_str = '--'
            season = '--'
        
        # Clear display
        self.lcd.clear()
        
        # Line 1: Title with timeframe (centered)
        title = f'AltSeason {timeframe}'
        title_pos = max(0, (16 - len(title)) // 2)
        self.lcd.cursor_pos = (0, title_pos)
        self.lcd.write_string(title[:16])
        
        # Line 2: Percentage and season indicator (centered)
        display_text = f"{value_str} - {season}"
        text_pos = max(0, (16 - len(display_text)) // 2)
        self.lcd.cursor_pos = (1, text_pos)
        self.lcd.write_string(display_text[:16])
        
        time.sleep(self.display_duration)

