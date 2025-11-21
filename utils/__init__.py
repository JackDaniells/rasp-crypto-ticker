"""
Utility functions for the crypto ticker application
"""


def format_large_number(value, decimal_places=None):
    """Format large numbers to readable strings with K/M/B/T suffixes
    
    Args:
        value: Numeric value to format
        decimal_places: Optional dict with keys 'T', 'B', 'M', 'K' for decimal places
                       Default: {'T': 2, 'B': 1, 'M': 1, 'K': 1}
    
    Returns:
        str: Formatted string (e.g., "1.2T", "450B", "25.5M") or "--" on error
    
    Examples:
        >>> format_large_number(1_234_567_890_000)
        '1.23T'
        >>> format_large_number(450_000_000_000)
        '450.0B'
        >>> format_large_number(25_500_000)
        '25.5M'
    """
    if value is None or value == '--':
        return '--'
    
    # Default decimal places for each magnitude
    if decimal_places is None:
        decimal_places = {'T': 2, 'B': 1, 'M': 1, 'K': 1}
    
    try:
        value = float(value)
        
        if value >= 1_000_000_000_000:  # Trillions
            decimals = decimal_places.get('T', 2)
            return f"{value / 1_000_000_000_000:.{decimals}f}T"
        elif value >= 1_000_000_000:  # Billions
            decimals = decimal_places.get('B', 1)
            return f"{value / 1_000_000_000:.{decimals}f}B"
        elif value >= 1_000_000:  # Millions
            decimals = decimal_places.get('M', 1)
            return f"{value / 1_000_000:.{decimals}f}M"
        elif value >= 1_000:  # Thousands
            decimals = decimal_places.get('K', 1)
            return f"{value / 1_000:.{decimals}f}K"
        else:
            return f"{value:.0f}"
    except (ValueError, TypeError):
        return '--'

