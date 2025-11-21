"""
CoinGecko Global API Client

Fetches global cryptocurrency market data from CoinGecko's /global endpoint
This includes total market cap, Bitcoin dominance, and market statistics

Implements internal caching to avoid duplicate API requests within a short time window

API Documentation: https://www.coingecko.com/api/documentation
"""

import requests
import time


# Internal cache to avoid duplicate requests
_cache = {
    'data': None,
    'timestamp': 0,
    'cache_duration': 60  # Cache duration in seconds (1 minute)
}


def get_global_data(timeout=10, force_refresh=False):
    """Fetch global cryptocurrency market data from CoinGecko API
    
    This function serves both Market Cap and BTC Dominance modules with a single
    API call. Results are cached for 1 minute to avoid duplicate requests.
    
    Args:
        timeout: Request timeout in seconds
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
    current_time = time.time()
    
    # Check if cache is still valid
    if not force_refresh and _cache['data'] is not None:
        cache_age = current_time - _cache['timestamp']
        if cache_age < _cache['cache_duration']:
            print(f"Global API: Using cached data (age: {cache_age:.1f}s)")
            return _cache['data']
    
    # Fetch fresh data
    url = "https://api.coingecko.com/api/v3/global"
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code != 200:
            print(f"Global API: Returned status {response.status_code}")
            return None
        
        data = response.json()
        
        if 'data' not in data:
            print("Global API: Invalid response structure")
            return None
        
        # Add timestamp to the data
        result = data['data']
        result['timestamp'] = int(current_time)
        
        # Update cache
        _cache['data'] = result
        _cache['timestamp'] = current_time
        
        print("Global API: Fresh data fetched and cached")
        
        return result
        
    except Exception as e:
        print(f"Global API: Error - {e}")
        return None

