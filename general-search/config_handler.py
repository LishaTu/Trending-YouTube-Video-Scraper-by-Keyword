"""
Configuration handler for YouTube Data Scraper
Manages API keys and configuration settings
"""
import os
import sys
from typing import Dict, Any


class ConfigHandler:
    """Handles configuration and API key management"""
    
    def __init__(self, api_key_path: str = 'api_key.txt'):
        """
        Initialize configuration handler
        
        Args:
            api_key_path: Path to the API key file
        """
        self.api_key_path = api_key_path
        self.api_key = None
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
                f"Please create a file named 'api_key.txt' with your YouTube API key."
            )
        
        with open(self.api_key_path, 'r') as f:
            api_key = f.read().strip()
        
        if not api_key:
            raise ValueError("API key file is empty. Please add your YouTube API key.")
        
        self.api_key = api_key
        return api_key
    
    def get_config(self) -> Dict[str, Any]:
        """Get configuration dictionary"""
        return self.config
    
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
