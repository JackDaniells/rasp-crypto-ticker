"""
Clients package for handling external API requests

All API clients use centralized caching via cache_utils to avoid code duplication.
"""

from .weather_api import get_weather
from .ip_api import get_ip_address
from .crypto_api import get_crypto_prices
from .fear_greed_api import get_fear_greed_index
from .coingecko_global_api import get_global_data
from .altcoin_season_api import get_altcoin_season_index
from .cache_utils import DEFAULT_CACHE_DURATION

__all__ = [
    'get_weather',
    'get_ip_address',
    'get_crypto_prices',
    'get_fear_greed_index',
    'get_global_data',
    'get_altcoin_season_index',
    'DEFAULT_CACHE_DURATION'
]

