"""
Altcoin Season Index API Client

Calculates the Altcoin Season Index using CoinGecko API
The index shows what percentage of the top 50 coins performed better than Bitcoin (BTC) 
over the last 90 days (or 30 days as fallback)
"""

import requests
import time


def get_altcoin_season_index(timeout=10):
    """Calculate Altcoin Season Index using CoinGecko API
    
    The index calculates the percentage of top 50 altcoins that outperformed 
    Bitcoin over the last 90 days. Based on this percentage:
    - 75% or more = Altcoin Season
    - 25% or less = Bitcoin Season
    - Between 25-75% = Mixed/Neutral
    
    Returns:
        dict: Altcoin Season data if successful, None otherwise
        Example response:
        {
            'value': 68,  # percentage of coins outperforming BTC
            'timestamp': 1640000000
        }
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    try:
        # Fetch top 50 coins with 30d price change data
        # Note: CoinGecko free API doesn't provide 90d data directly,
        # so we use 30d as a reasonable approximation
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 51,  # Top 50 + Bitcoin
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '30d'
        }
        
        response = requests.get(url, params=params, timeout=timeout)
        
        if response.status_code != 200:
            print(f"Altcoin Season API error: CoinGecko returned status code {response.status_code}")
            return None
        
        data = response.json()
        
        if not data or len(data) < 2:
            print("Altcoin Season: Insufficient data from CoinGecko")
            return None
        
        # Find Bitcoin's performance
        btc_performance = None
        altcoins = []
        
        for coin in data:
            coin_id = coin.get('id', '').lower()
            price_change = coin.get('price_change_percentage_30d_in_currency')
            
            if price_change is None:
                continue
                
            if coin_id == 'bitcoin':
                btc_performance = price_change
            else:
                altcoins.append({
                    'id': coin.get('id'),
                    'symbol': coin.get('symbol'),
                    'performance': price_change
                })
        
        if btc_performance is None:
            print("Altcoin Season: Bitcoin data not found")
            return None
        
        if len(altcoins) < 10:
            print(f"Altcoin Season: Not enough altcoins with data ({len(altcoins)})")
            return None
        
        # Count how many altcoins outperformed Bitcoin
        outperforming = sum(1 for coin in altcoins if coin['performance'] > btc_performance)
        total = len(altcoins)
        
        # Calculate percentage
        index_value = int((outperforming / total) * 100)
        
        print(f"Altcoin Season Index: {index_value}% ({outperforming}/{total} coins outperforming BTC)")
        
        return {
            'value': index_value,
            'timestamp': int(time.time())
        }
        
    except Exception as e:
        print(f"Error calculating altcoin season index: {e}")
        return None

