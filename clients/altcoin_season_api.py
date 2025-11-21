"""
Altcoin Season Index API Client

Calculates the Altcoin Season Index using CoinGecko API
The index shows what percentage of the top 100 coins performed better than Bitcoin (BTC) 
over the last 7 days and 30 days

Implementation uses a reusable _calculate_index() helper method to avoid code duplication
when calculating indices for multiple timeframes.
"""

import requests
import time


def _calculate_index(altcoins, btc_performance, performance_key, timeframe_label):
    """Calculate Altcoin Season Index for a specific timeframe
    
    Args:
        altcoins: List of altcoin data dictionaries
        btc_performance: Bitcoin's performance percentage for this timeframe
        performance_key: Key to access performance data (e.g., 'performance_7d')
        timeframe_label: Label for logging (e.g., '7d', '30d')
    
    Returns:
        int: Index percentage (0-100), or None if calculation fails
    """
    if btc_performance is None:
        return None
    
    # Filter altcoins that have data for this timeframe
    altcoins_with_data = [c for c in altcoins if c[performance_key] is not None]
    
    if len(altcoins_with_data) == 0:
        return None
    
    # Count how many altcoins outperformed Bitcoin
    outperforming = sum(1 for coin in altcoins_with_data if coin[performance_key] > btc_performance)
    total = len(altcoins_with_data)
    
    # Calculate percentage
    index_value = int((outperforming / total) * 100)
    
    # Log result
    print(f"Altcoin Season {timeframe_label}: {index_value}% ({outperforming}/{total} coins outperforming BTC)")
    
    return index_value


def get_altcoin_season_index(timeout=10):
    """Calculate Altcoin Season Index using CoinGecko API for both 7d and 30d
    
    The index calculates the percentage of top 100 altcoins that outperformed 
    Bitcoin over the last 7 days and 30 days. Based on this percentage:
    - 75% or more = Altcoin Season
    - 25% or less = Bitcoin Season
    - Between 25-75% = Mixed/Neutral
    
    Returns:
        dict: Altcoin Season data if successful, None otherwise
        Example response:
        {
            'value_7d': 68,     # 7d percentage
            'value_30d': 52,    # 30d percentage
            'timestamp': 1640000000
        }
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    try:
        # Fetch top 110 coins with both 24h and 30d price change data
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 110,  # Fetch extra to ensure 100 altcoins with data
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '7d,30d'
        }
        
        response = requests.get(url, params=params, timeout=timeout)
        
        if response.status_code != 200:
            print(f"Altcoin Season API error: CoinGecko returned status code {response.status_code}")
            return None
        
        data = response.json()
        
        if not data or len(data) < 2:
            print("Altcoin Season: Insufficient data from CoinGecko")
            return None
        
        # Find Bitcoin's performance and collect altcoins for both timeframes
        btc_performance_7d = None
        btc_performance_30d = None
        altcoins = []
        
        for coin in data:
            coin_id = coin.get('id', '').lower()
            price_change_7d = coin.get('price_change_percentage_7d_in_currency')
            price_change_30d = coin.get('price_change_percentage_30d_in_currency')
            
            # Skip if both values are missing
            if price_change_7d is None and price_change_30d is None:
                continue
                
            if coin_id == 'bitcoin':
                btc_performance_7d = price_change_7d
                btc_performance_30d = price_change_30d
            else:
                altcoins.append({
                    'id': coin.get('id'),
                    'symbol': coin.get('symbol'),
                    'performance_7d': price_change_7d,
                    'performance_30d': price_change_30d
                })
        
        if btc_performance_7d is None and btc_performance_30d is None:
            print("Altcoin Season: Bitcoin data not found")
            return None
        
        # Take only the first 100 altcoins (they're already ordered by market cap)
        altcoins = altcoins[:100]
        
        if len(altcoins) < 100:
            print(f"Altcoin Season: Only {len(altcoins)} altcoins with data (target: 100)")
        
        # Calculate 7d index
        index_7d = _calculate_index(altcoins, btc_performance_7d, 'performance_7d', '7d')
        
        # Calculate 30d index
        index_30d = _calculate_index(altcoins, btc_performance_30d, 'performance_30d', '30d')
        
        if index_7d is None and index_30d is None:
            print("Altcoin Season: Failed to calculate any index")
            return None
        
        return {
            'value_7d': index_7d,
            'value_30d': index_30d,
            'timestamp': int(time.time())
        }
        
    except Exception as e:
        print(f"Error calculating altcoin season index: {e}")
        return None

