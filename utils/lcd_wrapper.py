"""
LCD Wrapper with automatic text validation

Wraps the RPLCD CharLCD class to automatically truncate text that exceeds
the LCD's maximum width (16 characters for 16x2 displays).

This prevents display corruption from overly long text strings.
"""

# Row constants for LCD lines
ROW_FIRST = 0
ROW_SECOND = 1

# Position constants for text alignment
POS_LEFT = 'left'
POS_CENTER = 'center'
POS_RIGHT = 'right'


class SafeLCD:
    """
    Wrapper for CharLCD that automatically validates text length
    
    Automatically truncates any text written to the LCD to prevent overflow.
    All other CharLCD methods and properties are passed through unchanged.
    """
    
    def __init__(self, lcd, max_size):
        """
        Initialize SafeLCD wrapper
        
        Args:
            lcd: The CharLCD instance to wrap
            max_size: Maximum characters per line (required)
        """
        self._lcd = lcd
        self._max_size = max_size
    
    def write_string(self, *, row=0, text='', pos=POS_LEFT):
        """
        Write string to LCD with automatic length validation and positioning
        
        Args:
            row: Row number (0 for first line, 1 for second line)
            text: Text to write (will be truncated to max_size if needed)
            pos: Text position - POS_LEFT, POS_CENTER, or POS_RIGHT (default: POS_LEFT)
        
        Note:
            All parameters must be specified by name (keyword arguments)
            Examples:
                lcd.write_string(row=0, text='Hello', pos=POS_LEFT)
                lcd.write_string(row=1, text='World', pos=POS_CENTER)
                lcd.write_string(row=0, text='$99.99', pos=POS_RIGHT)
        """
        validated_text = str(text)[:self._max_size]
        
        # Calculate column position based on alignment
        if pos == POS_CENTER:
            col = max(0, round((self._max_size - len(validated_text)) / 2))
        elif pos == POS_RIGHT:
            col = max(0, self._max_size - len(validated_text))
        else:  # POS_LEFT or any other value defaults to left
            col = 0
        
        self._lcd.cursor_pos = (row, col)
        self._lcd.write_string(validated_text)
    
    def __getattr__(self, name):
        """
        Pass through all other attributes/methods to the wrapped LCD
        
        This allows SafeLCD to act as a transparent wrapper - any method
        or property not explicitly defined here will be forwarded to the
        underlying CharLCD instance.
        """
        return getattr(self._lcd, name)

