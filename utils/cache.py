"""
Cache Utilities

Provides reusable caching functionality for API clients to avoid code duplication.
"""

import time
from functools import wraps


# Default cache durations (in seconds)
DEFAULT_CACHE_DURATION = 600  # 10 minutes


def create_cache():
    """
    Create a cache dictionary with standard structure
    
    Returns:
        dict: Cache dictionary with data, timestamp, and duration fields
    """
    return {
        'data': None,
        'timestamp': 0,
        'cache_duration': DEFAULT_CACHE_DURATION,
        'key': None  # Optional key for multi-tenant caching
    }


def is_cache_valid(cache, cache_duration=None, cache_key=None):
    """
    Check if cache is still valid
    
    Args:
        cache: Cache dictionary
        cache_duration: Override cache duration (uses cache['cache_duration'] if None)
        cache_key: Optional key for multi-tenant caching
    
    Returns:
        bool: True if cache is valid, False otherwise
    """
    if cache['data'] is None:
        return False
    
    # Check cache key if provided
    if cache_key is not None and cache.get('key') != cache_key:
        return False
    
    # Check cache age
    current_time = time.time()
    duration = cache_duration if cache_duration is not None else cache.get('cache_duration', DEFAULT_CACHE_DURATION)
    cache_age = current_time - cache['timestamp']
    
    return cache_age < duration


def update_cache(cache, data, cache_duration=None, cache_key=None):
    """
    Update cache with new data
    
    Args:
        cache: Cache dictionary to update
        data: Data to cache
        cache_duration: Cache duration in seconds
        cache_key: Optional key for multi-tenant caching
    """
    current_time = time.time()
    cache['data'] = data
    cache['timestamp'] = current_time
    
    if cache_duration is not None:
        cache['cache_duration'] = cache_duration
    
    if cache_key is not None:
        cache['key'] = cache_key


def get_cache_age(cache):
    """
    Get the age of cached data in seconds
    
    Args:
        cache: Cache dictionary
    
    Returns:
        float: Age in seconds, or None if no cached data
    """
    if cache['data'] is None:
        return None
    
    return time.time() - cache['timestamp']


def cached_api_call(cache, fetch_function, cache_duration=DEFAULT_CACHE_DURATION, 
                   cache_key=None, force_refresh=False, api_name="API"):
    """
    Generic cached API call handler
    
    This function encapsulates the common caching pattern used across all API clients:
    1. Check if cache is valid
    2. If valid, return cached data
    3. If not, fetch fresh data and update cache
    
    Args:
        cache: Cache dictionary
        fetch_function: Function to call to fetch fresh data (should return data or None)
        cache_duration: Cache duration in seconds
        cache_key: Optional key for multi-tenant caching
        force_refresh: If True, bypasses cache
        api_name: Name of the API for logging
    
    Returns:
        Data from cache or fresh API call
    """
    # Check if cache is valid
    if not force_refresh and is_cache_valid(cache, cache_duration, cache_key):
        cache_age = get_cache_age(cache)
        print(f"{api_name}: Using cached data (age: {cache_age:.1f}s)")
        return cache['data']
    
    # Fetch fresh data
    data = fetch_function()
    
    if data is not None:
        print(f"{api_name}: Fresh data fetched")
        update_cache(cache, data, cache_duration, cache_key)
    
    return data

