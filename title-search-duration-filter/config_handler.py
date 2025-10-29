"""
Configuration handler for YouTube Data Scraper
Manages API keys, configuration settings, and quota tracking
"""
import os
import sys
import json
from typing import Dict, Any
from datetime import datetime, timedelta


class ConfigHandler:
    """Handles configuration and API key management"""
    
    def __init__(self, api_key_path: str = 'api_key.text'):
        """
        Initialize configuration handler
        
        Args:
            api_key_path: Path to the API key file
        """
        self.api_key_path = api_key_path
        self.api_key = None
        self.quota_file = 'quota_usage.json'
        self.daily_quota_limit = 10000  # YouTube default
        self.quota_usage = self.load_quota_usage()
        
        self.config = {
            'max_results_per_page': 50,
            'default_region': 'US',
            'quota_cost': {
                'search': 100,
                'videos_list': 1
            }
        }
    
    def load_api_key(self) -> str:
        """
        Load API key from file
        
        Returns:
            API key string
            
        Raises:
            FileNotFoundError: If API key file doesn't exist
            ValueError: If API key file is empty
        """
        if not os.path.exists(self.api_key_path):
            raise FileNotFoundError(
                f"API key file not found at: {self.api_key_path}\n"
                f"Please create a file named 'api_key.text' with your YouTube API key."
            )
        
        with open(self.api_key_path, 'r') as f:
            api_key = f.read().strip()
        
        if not api_key:
            raise ValueError("API key file is empty. Please add your YouTube API key.")
        
        self.api_key = api_key
        return api_key
    
    def load_quota_usage(self) -> Dict[str, Any]:
        """Load quota usage from file"""
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r') as f:
                data = json.load(f)
                # Reset if it's a new day
                last_reset = datetime.fromisoformat(data.get('last_reset', datetime.now().isoformat()))
                if last_reset.date() < datetime.now().date():
                    return self.reset_quota()
                return data
        else:
            return self.reset_quota()
    
    def reset_quota(self) -> Dict[str, Any]:
        """Reset quota usage for a new day"""
        return {
            'used': 0,
            'last_reset': datetime.now().isoformat(),
            'operations': []
        }
    
    def save_quota_usage(self):
        """Save quota usage to file"""
        with open(self.quota_file, 'w') as f:
            json.dump(self.quota_usage, f, indent=2)
    
    def check_quota_availability(self, required_units: int) -> tuple:
        """
        Check if enough quota is available
        
        Args:
            required_units: Units needed for operation
            
        Returns:
            Tuple of (is_available, remaining_quota)
        """
        remaining = self.daily_quota_limit - self.quota_usage['used']
        return remaining >= required_units, remaining
    
    def use_quota(self, units: int, operation: str):
        """
        Record quota usage
        
        Args:
            units: Quota units used
            operation: Description of operation
        """
        self.quota_usage['used'] += units
        self.quota_usage['operations'].append({
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'units': units
        })
        self.save_quota_usage()
        
        # Print quota status
        remaining = self.daily_quota_limit - self.quota_usage['used']
        percentage = (self.quota_usage['used'] / self.daily_quota_limit) * 100
        print(f"Quota used: {self.quota_usage['used']}/{self.daily_quota_limit} ({percentage:.1f}%) - Remaining: {remaining}")
    
    def get_quota_summary(self) -> Dict[str, Any]:
        """Get current quota usage summary"""
        return {
            'used': self.quota_usage['used'],
            'limit': self.daily_quota_limit,
            'remaining': self.daily_quota_limit - self.quota_usage['used'],
            'percentage': (self.quota_usage['used'] / self.daily_quota_limit) * 100
        }
    
    def estimate_quota_usage(self, num_searches: int, num_videos: int) -> int:
        """
        Estimate API quota usage
        
        Args:
            num_searches: Number of search requests
            num_videos: Number of video detail requests
            
        Returns:
            Total estimated quota units
        """
        search_cost = num_searches * self.config['quota_cost']['search']
        videos_cost = num_videos * self.config['quota_cost']['videos_list']
        return search_cost + videos_cost