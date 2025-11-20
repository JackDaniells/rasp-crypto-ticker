"""IP API Client - Handles HTTP requests to IP address service"""

import requests


def get_ip_address(timeout=10):
    """
    Fetch public IP address from ipify API
    
    Args:
        timeout: Request timeout in seconds
        
    Returns:
        IP address string if successful, None if failed
    """
    url = "https://api.ipify.org"
    params = {'format': 'json'}
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            if 'ip' in data:
                print(f"Public IP: {data['ip']}")
                return data['ip']
            else:
                print("IP address not found in response")
                return None
        else:
            print(f"IP API error: status code {response.status_code}")
            return None

    except Exception as e:
        print(f"Unexpected error fetching IP address: {e}")
        return None

