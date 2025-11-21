"""Weather API Client - Handles HTTP requests to WeatherAPI"""

import requests
from utils.cache import create_cache, cached_api_call, DEFAULT_CACHE_DURATION


# Internal cache
_cache = create_cache()


def get_weather(api_key, location, timeout=10, cache_duration=DEFAULT_CACHE_DURATION, force_refresh=False):
    """
    Fetch weather data from WeatherAPI with caching
    
    Args:
        api_key: WeatherAPI key
        location: Location IP or name
        timeout: Request timeout in seconds
        cache_duration: Cache duration in seconds (default: 600 = 10 minutes)
        force_refresh: If True, bypasses cache
        
    Returns:
        Weather data dict if successful, None if failed
    """
    cache_key = f"{api_key}_{location}"
    
    # Define fetch function
    def fetch():
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            'q': location,
            'key': api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                print(f"- {data.get('location', {}).get('name', 'Unknown')}")
                return data
            else:
                print(f"Weather API error: {url} returned status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Unexpected error fetching weather data: {e}")
            return None
    
    # Use centralized caching
    return cached_api_call(
        cache=_cache,
        fetch_function=fetch,
        cache_duration=cache_duration,
        cache_key=cache_key,
        force_refresh=force_refresh,
        api_name="Weather API"
    )

