"""
Fear and Greed Index API Client

Fetches cryptocurrency fear and greed index from Alternative.me
API Documentation: https://alternative.me/crypto/fear-and-greed-index/
"""

import requests


def get_fear_greed_index(timeout=10):
    """Fetch Fear and Greed Index from Alternative.me API
    
    The index ranges from 0 (Extreme Fear) to 100 (Extreme Greed)
    
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
    url = "https://api.alternative.me/fng/"
    
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            # API returns {"data": [{"value": "45", ...}]}
            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]
            return None
        else:
            print(f"Fear & Greed API error: {url} returned status code {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error fetching Fear & Greed Index: {e}")
        return None

