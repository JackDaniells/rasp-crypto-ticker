"""
Fear and Greed Index API Client

Fetches cryptocurrency fear and greed index from Alternative.me
API Documentation: https://alternative.me/crypto/fear-and-greed-index/
"""

import requests
from utils.cache import create_cache, cached_api_call, DEFAULT_CACHE_DURATION


# Internal cache
_cache = create_cache()


def get_fear_greed_index(timeout=10, cache_duration=DEFAULT_CACHE_DURATION, force_refresh=False):
    """Fetch Fear and Greed Index from Alternative.me API with caching
    
    The index ranges from 0 (Extreme Fear) to 100 (Extreme Greed)
    
    Args:
        timeout: Request timeout in seconds
        cache_duration: Cache duration in seconds (default: 3600 = 1 hour)
        force_refresh: If True, bypasses cache
    
    Returns:
        dict: Fear and Greed data if successful, None otherwise
        Example response:
        {
            'value': '45',
            'value_classification': 'Fear',
            'timestamp': '1234567890',
            'time_until_update': '43200'
        }
    """
    # Define fetch function
    def fetch():
        url = "https://api.alternative.me/fng/"
        
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                # API returns {"data": [{"value": "45", ...}]}
                if 'data' in data and len(data['data']) > 0:
                    result = data['data'][0]
                    print(f"- Index: {result.get('value')}")
                    return result
                return None
            else:
                print(f"Fear & Greed API error: {url} returned status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching Fear & Greed Index: {e}")
            return None
    
    # Use centralized caching
    return cached_api_call(
        cache=_cache,
        fetch_function=fetch,
        cache_duration=cache_duration,
        force_refresh=force_refresh,
        api_name="Fear & Greed API"
    )

