"""
Altcoin Season Module

Displays the Altcoin Season Index which shows what percentage of the top 50 
coins performed better than Bitcoin over the last 30 days.

Calculated using CoinGecko API data (free, no API key required).

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
            index_value: Percentage of top 50 coins that outperformed Bitcoin (0-100)
        
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
        """Display Altcoin Season Index on LCD"""
        if not self.is_data_ready():
            return
        
        # Get altcoin season index value
        index_value = self.data.get('value', '--')
        
        # Format index value and determine season
        if index_value != '--':
            try:
                index_str = f"{int(index_value)}%"
                season = self._get_season(int(index_value))
            except (ValueError, TypeError):
                index_str = '--'
                season = '--'
        else:
            index_str = '--'
            season = '--'
        
        # Display Altcoin Season Index
        self.lcd.clear()
        
        # Line 1: Title (centered)
        title = 'Altcoin Season'
        title_pos = (16 - len(title)) // 2
        self.lcd.cursor_pos = (0, title_pos)
        self.lcd.write_string(title)
        
        # Line 2: Index percentage (left) and season indicator (right)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(index_str)
        
        # Right-align season indicator
        season_pos = 16 - len(season)
        self.lcd.cursor_pos = (1, season_pos)
        self.lcd.write_string(season)
        
        time.sleep(self.display_duration)

