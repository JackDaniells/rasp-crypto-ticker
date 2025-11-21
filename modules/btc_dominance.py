"""
Bitcoin Dominance Module

Displays Bitcoin's dominance in the cryptocurrency market.
Bitcoin dominance is the percentage of total crypto market cap that Bitcoin represents.

Higher dominance (>50%) often indicates Bitcoin Season
Lower dominance (<40%) often indicates Altcoin Season
"""

import time
from .base import BaseModule
from clients import get_global_data
from utils.lcd_wrapper import POS_CENTER, ROW_FIRST, ROW_SECOND


class BtcDominanceModule(BaseModule):
    """Module for displaying Bitcoin Dominance"""
    
    def __init__(self, lcd, config):
        super().__init__('BTC Dominance', lcd, config)
        self.timeout = config.get('timeout', 10)
    
    def fetch_data(self):
        """Fetch Bitcoin dominance from CoinGecko API"""
        data = get_global_data(timeout=self.timeout, cache_duration=self.update_interval)
        
        if data is None:
            return None
        
        # Extract BTC dominance from global data
        if 'market_cap_percentage' not in data:
            print("BTC Dominance: market_cap_percentage not in response")
            return None
        
        btc_dominance = data['market_cap_percentage'].get('btc')
        
        if btc_dominance is None:
            print("BTC Dominance: Bitcoin data not found")
            return None
        
        print(f"BTC Dominance: {btc_dominance:.2f}%")
        
        return {
            'dominance': round(btc_dominance, 2),
            'timestamp': data.get('timestamp', int(time.time()))
        }
    
    def _get_status(self, dominance):
        """Determine market status based on dominance
        
        Args:
            dominance: Bitcoin dominance percentage (0-100)
        
        Returns:
            str: Status classification
        """
        if dominance >= 55:
            return "Very High"
        elif dominance >= 50:
            return "High"
        elif dominance >= 45:
            return "Moderate"
        elif dominance >= 40:
            return "Low"
        else:
            return "Very Low"
    
    def display(self):
        """Display Bitcoin Dominance on LCD"""
        if not self.is_data_ready():
            return
        
        # Get dominance value
        dominance = self.data.get('dominance')
        
        if dominance is not None:
            try:
                dominance_str = f"{int(round(dominance))}%"
                status = self._get_status(dominance)
            except (ValueError, TypeError):
                dominance_str = '--'
                status = '--'
        else:
            dominance_str = '--'
            status = '--'
        
        # Clear display
        self.lcd.clear()
        
        # Line 1: Title (centered)
        title = 'BTC Dominance'
        self.lcd.write_string(row=ROW_FIRST, text=title, pos=POS_CENTER)
        
        # Line 2: Dominance percentage and status (centered)
        display_text = f"{dominance_str} - {status}"
        self.lcd.write_string(row=ROW_SECOND, text=display_text, pos=POS_CENTER)
        
        time.sleep(self.display_duration)

