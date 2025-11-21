"""Crypto API Client - Handles HTTP requests to CoinGecko API"""

import requests
from utils.cache import create_cache, cached_api_call, DEFAULT_CACHE_DURATION


# Internal cache
_cache = create_cache()


def get_crypto_prices(crypto_ids, fiat_currency='usd', timeout=10, cache_duration=DEFAULT_CACHE_DURATION, force_refresh=False):
    """
    Fetch cryptocurrency prices from CoinGecko API with caching
    
    Args:
        crypto_ids: Comma-separated string or list of cryptocurrency IDs
        fiat_currency: Fiat currency code (e.g., 'usd', 'eur')
        timeout: Request timeout in seconds
        cache_duration: Cache duration in seconds (default: 600 = 10 minutes)
        force_refresh: If True, bypasses cache
        
    Returns:
        Crypto price data dict if successful, None if failed
    """
    # Convert list to comma-separated string if needed
    if isinstance(crypto_ids, list):
        crypto_ids = ','.join(crypto_ids)
    
    cache_key = f"{crypto_ids}_{fiat_currency}"
    
    # Define fetch function
    def fetch():
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': crypto_ids,
            'vs_currencies': fiat_currency,
            'include_24hr_change': 'true',
            'precision': '2'
        }
        
        try:
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                print(f"- {list(data.keys())}")
                return data
            else:
                print(f"Crypto API error: {url} returned status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Unexpected error fetching crypto data: {e}")
            return None
    
    # Use centralized caching
    return cached_api_call(
        cache=_cache,
        fetch_function=fetch,
        cache_duration=cache_duration,
        cache_key=cache_key,
        force_refresh=force_refresh,
        api_name="Crypto API"
    )

