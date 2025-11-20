"""Crypto API Client - Handles HTTP requests to CoinGecko API"""

import requests


def get_crypto_prices(coingecko_ids, fiat_currency='usd', timeout=10):
    """
    Fetch cryptocurrency prices from CoinGecko API
    
    Args:
        coingecko_ids: Comma-separated string or list of CoinGecko IDs
        fiat_currency: Fiat currency code (e.g., 'usd', 'eur')
        timeout: Request timeout in seconds
        
    Returns:
        Crypto price data dict if successful, None if failed
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    # Convert list to comma-separated string if needed
    if isinstance(coingecko_ids, list):
        coingecko_ids = ','.join(coingecko_ids)
    
    params = {
        'ids': coingecko_ids,
        'vs_currencies': fiat_currency,
        'include_24hr_change': 'true',
        'precision': '2'
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            print(f"Crypto data fetched: {list(data.keys())}")
            return data
        else:
            print(f"Crypto API error: {url} returned status code {response.status_code}")
            return None
              
    except Exception as e:
        print(f"Unexpected error fetching crypto data: {e}")
        return None

