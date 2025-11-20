"""Clients package for handling external API requests"""

from .weather_api import get_weather
from .ip_api import get_ip_address
from .crypto_api import get_crypto_prices

__all__ = ['get_weather', 'get_ip_address', 'get_crypto_prices']

