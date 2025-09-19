"""
Search handler for YouTube videos
Manages search queries and result collection
"""
from typing import List, Dict, Any, Optional
from youtube_client import YouTubeClient
import time


class SearchHandler:
    """Handles YouTube search operations"""
    
    def __init__(self, youtube_client: YouTubeClient):
        """
        Initialize search handler
        
        Args:
            youtube_client: Initialized YouTube API client
        """
        self.client = youtube_client
        self.search_results = []
        self.video_details = []
    
    def search_videos_with_keywords(self, keywords: List[str], 
                                  max_total_results: int = 100,
                                  order: str = 'viewCount',
                                  published_after: Optional[str] = None,
                                  published_before: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search videos with multiple keywords
        
        Args:
            keywords: List of keywords to search
            max_total_results: Maximum total results to fetch across all pages (not per page)
            order: Sort order
            published_after: RFC 3339 formatted date-time
            published_before: RFC 3339 formatted date-time
            
        Returns:
            List of video items
        """
        query = ' '.join(keywords)
        all_videos = []
        next_page_token = None
        
        print(f"Searching for: '{query}'")
        
        while len(all_videos) < max_total_results:
            try:
                # Search for videos
                response = self.client.search_videos(
                    query=query,
                    max_results=min(50, max_total_results - len(all_videos)),
                    order=order,
                    page_token=next_page_token,
                    published_after=published_after,
                    published_before=published_before
                )
                
                videos = response.get('items', [])
                all_videos.extend(videos)
                
                print(f"Fetched {len(videos)} videos (Total: {len(all_videos)})")
                
                # Check for next page
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error during search: {str(e)}")
                break
        
        self.search_results = all_videos
        return all_videos
    
    def fetch_video_statistics(self, video_items: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """
        Fetch detailed statistics for videos
        
        Args:
            video_items: List of video items from search (uses stored results if None)
            
        Returns:
            List of videos with full details
        """
        if video_items is None:
            video_items = self.search_results
        
        if not video_items:
            return []
        
        all_details = []
        
        # Process in batches of 50 (API limit)
        for i in range(0, len(video_items), 50):
            batch = video_items[i:i + 50]
            video_ids = [item['id']['videoId'] for item in batch]
            
            try:
                response = self.client.get_video_details(video_ids)
                details = response.get('items', [])
                all_details.extend(details)
                
                print(f"Fetched statistics for {len(details)} videos")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching video details: {str(e)}")
        
        self.video_details = all_details
        return all_details
    
    
    def search_and_get_details(self, keywords: List[str], 
                             max_results: int = 100,
                             published_after: Optional[str] = None,
                             published_before: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Combined search and detail fetching
        
        Args:
            keywords: Keywords to search
            max_results: Maximum results
            published_after: RFC 3339 formatted date-time
            published_before: RFC 3339 formatted date-time
            
        Returns:
            List of videos with full details
        """
        # Search for videos
        search_results = self.search_videos_with_keywords(
            keywords, 
            max_results,
            published_after=published_after,
            published_before=published_before
        )
        
        # Get detailed statistics
        detailed_results = self.fetch_video_statistics(search_results)
        
        return detailed_results