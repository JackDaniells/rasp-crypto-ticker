"""
CoinGecko Global API Client

Fetches global cryptocurrency market data from CoinGecko's /global endpoint
This includes total market cap, Bitcoin dominance, and market statistics

Implements internal caching to avoid duplicate API requests within a short time window

API Documentation: https://www.coingecko.com/api/documentation
"""

import requests
import time
from utils.cache import create_cache, cached_api_call, DEFAULT_CACHE_DURATION


# Internal cache to avoid duplicate requests
_cache = create_cache()


def get_global_data(timeout=10, cache_duration=DEFAULT_CACHE_DURATION, force_refresh=False):
    """Fetch global cryptocurrency market data from CoinGecko API with caching
    
    This function serves both Market Cap and BTC Dominance modules with a single
    API call. Results are cached to avoid duplicate requests.
    
    Args:
        timeout: Request timeout in seconds
        cache_duration: Cache duration in seconds (default: 600 = 10 minutes)
        force_refresh: If True, bypasses cache and fetches fresh data
    
    Returns:
        dict: Global market data if successful, None otherwise
        Example response:
        {
            'total_market_cap': {'usd': 1234567890000, ...},
            'total_volume': {'usd': 123456789000, ...},
            'market_cap_percentage': {'btc': 45.5, 'eth': 18.2, ...},
            'market_cap_change_percentage_24h_usd': 2.5,
            'timestamp': 1640000000  # Added by this function
        }
    """
    # Define fetch function
    def fetch():
        url = "https://api.coingecko.com/api/v3/global"
        
        try:
            response = requests.get(url, timeout=timeout)
            
            if response.status_code != 200:
                print(f"Coingecko Global API: Returned status {response.status_code}")
                return None
            
            data = response.json()
            
            if 'data' not in data:
                print("Coingecko Global API: Invalid response structure")
                return None
            
            # Add timestamp to the data
            result = data['data']
            result['timestamp'] = int(time.time())
            
            print("- Market data fetched")
            return result
            
        except Exception as e:
            print(f"Coingecko Global API: Error - {e}")
            return None
    
    # Use centralized caching
    return cached_api_call(
        cache=_cache,
        fetch_function=fetch,
        cache_duration=cache_duration,
        force_refresh=force_refresh,
        api_name="Coingecko Global API"
    )

