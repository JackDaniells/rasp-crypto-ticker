"""
Crypto Market Cap API Client

Fetches global cryptocurrency market capitalization from CoinGecko
API Documentation: https://www.coingecko.com/api/documentation
"""

import requests


def get_global_market_cap(timeout=10):
    """Fetch global cryptocurrency market data from CoinGecko API
    
    Returns:
        dict: Global market data if successful, None otherwise
        Example response:
        {
            'total_market_cap': {'usd': 1234567890000, ...},
            'total_volume': {'usd': 123456789000, ...},
            'market_cap_percentage': {'btc': 45.5, 'eth': 18.2, ...},
            'market_cap_change_percentage_24h_usd': 2.5
        }
    """
    url = "https://api.coingecko.com/api/v3/global"
    
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            # API returns {"data": {...}}
            if 'data' in data:
                return data['data']
            return None
        else:
            print(f"Market Cap API error: {url} returned status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching global market cap: {e}")
        return None

