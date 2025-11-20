"""Weather API Client - Handles HTTP requests to WeatherAPI"""

import requests


def get_weather(api_key, location, timeout=10):
    """
    Fetch weather data from WeatherAPI
    
    Args:
        api_key: WeatherAPI key
        location: Location IP or name
        timeout: Request timeout in seconds
        
    Returns:
        Weather data dict if successful, None if failed
    """
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'q': location,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            print(f"Weather data fetched: {data.get('location', {}).get('name', 'Unknown')}")
            return data
        else:
            print(f"Weather API error: {url} returned status code {response.status_code}")
            return None
            
        
    except Exception as e:
        print(f"Unexpected error fetching weather data: {e}")
        return None

