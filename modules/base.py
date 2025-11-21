"""Base module class for all display modules"""

from abc import ABC, abstractmethod
from datetime import datetime


class BaseModule(ABC):
    """Abstract base class for all display modules"""
    
    def __init__(self, name, lcd, config):
        """
        Initialize base module
        
        Args:
            name: Module name
            lcd: LCD display object
            config: Configuration dictionary
        """
        self.name = name
        self.lcd = lcd
        self.config = config
        
        # Validate required base configuration
        required_keys = ['enabled', 'update_interval', 'display_duration', 'max_failed_attempts']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"{name} module missing required config keys: {', '.join(missing_keys)}. Check config.py")
        
        self.enabled = config['enabled']
        self.update_interval = config['update_interval']  # seconds
        self.display_duration = config['display_duration']  # seconds
        self.max_failed_attempts = config['max_failed_attempts']
        self.last_update = 0
        self.data = {}
        self.consecutive_failures = 0
    
    @abstractmethod
    def fetch_data(self):
        """Fetch data for this module (to be implemented by subclasses)"""
        pass
    
    @abstractmethod
    def display(self):
        """Display module data (to be implemented by subclasses)"""
        pass
    
    def is_error_data(self, data):
        """
        Check if data is None or empty (indicating API failure)
        Modules handle missing fields with dummy values during display
        """
        return data is None or data == {}
    
    def should_update_data(self):
        """Check if data should be updated based on interval"""
        current_time = datetime.now().timestamp()
        return (current_time - self.last_update) >= self.update_interval
    
    def is_data_ready(self):
        """
        Check if data is ready for display, updating if necessary
        
        Returns:
            bool: True if data is available, False otherwise
        """
        if not self.data:
            self.update_data()
            if not self.data:
                return False
        return True
    
    def update_data(self):
        """
        Update module data and timestamp
        
        Keeps last good data on API failure until max_failed_attempts is reached
        """
        if self.should_update_data():
            new_data = self.fetch_data()
            
            # Check if new data is valid or error
            if self.is_error_data(new_data):
                self.consecutive_failures += 1
                print(f"{self.name} module: API failure {self.consecutive_failures}/{self.max_failed_attempts}")
                
                # Only replace good data with error after max failures
                if self.consecutive_failures >= self.max_failed_attempts:
                    print(f"{self.name} module: Max failures reached, showing error")
                    self.data = new_data
                else:
                    print(f"{self.name} module: Keeping previous data")
                    # Keep self.data as-is (previous good data)
            else:
                # Success! Reset failure counter and update data
                self.consecutive_failures = 0
                self.data = new_data
                print(f"{self.name} module: Data updated successfully")
            
            self.last_update = datetime.now().timestamp()
    
    def is_enabled(self):
        """Check if module is enabled"""
        return self.enabled
    
    def get_display_count(self):
        """Return number of screens this module will display"""
        return 1

