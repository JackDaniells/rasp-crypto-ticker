"""Clients package for handling external API requests"""

from .weather_api import get_weather
from .ip_api import get_ip_address
from .crypto_api import get_crypto_prices
from .fear_greed_api import get_fear_greed_index
from .market_cap_api import get_global_market_cap

__all__ = [
    'get_weather',
    'get_ip_address',
    'get_crypto_prices',
    'get_fear_greed_index',
    'get_global_market_cap'
]

