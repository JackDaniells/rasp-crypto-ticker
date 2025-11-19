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
        self.enabled = config.get('enabled', True)
        self.update_interval = config.get('update_interval', 600)  # seconds
        self.display_duration = config.get('display_duration', 10)  # seconds
        self.last_update = 0
        self.data = {}
    
    @abstractmethod
    def fetch_data(self):
        """Fetch data for this module (to be implemented by subclasses)"""
        pass
    
    @abstractmethod
    def display(self):
        """Display module data (to be implemented by subclasses)"""
        pass
    
    def should_update_data(self):
        """Check if data should be updated based on interval"""
        current_time = datetime.now().timestamp()
        return (current_time - self.last_update) >= self.update_interval
    
    def update_data(self):
        """Update module data and timestamp"""
        if self.should_update_data():
            self.data = self.fetch_data()
            self.last_update = datetime.now().timestamp()
    
    def is_enabled(self):
        """Check if module is enabled"""
        return self.enabled
    
    def get_display_count(self):
        """Return number of screens this module will display"""
        return 1

