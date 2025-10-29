"""
YouTube API client wrapper
Handles API initialization and basic requests
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Optional, Dict, Any
import time


class YouTubeClient:
    """Wrapper for YouTube Data API v3"""
    
    def __init__(self, api_key: str):
        """
        Initialize YouTube client
        
        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the YouTube API client"""
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        except Exception as e:
            raise Exception(f"Failed to initialize YouTube client: {str(e)}")
    
    def search_videos(self, query: str, max_results: int = 50, 
                     order: str = 'viewCount', region_code: str = 'US',
                     page_token: Optional[str] = None,
                     published_after: Optional[str] = None,
                     published_before: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for videos on YouTube
        
        Args:
            query: Search query string
            max_results: Maximum results per page (max 50)
            order: Sort order (viewCount, relevance, date, rating, title)
            region_code: Region code for results
            page_token: Token for pagination
            published_after: RFC 3339 formatted date-time (e.g., '2024-01-01T00:00:00Z')
            published_before: RFC 3339 formatted date-time
            
        Returns:
            API response dictionary
        """
        try:
            # Build request parameters
            params = {
                'q': query,
                'part': 'snippet',
                'type': 'video',
                'order': order,
                'maxResults': max_results,
                'regionCode': region_code
            }
            
            # Add optional parameters
            if page_token:
                params['pageToken'] = page_token
            if published_after:
                params['publishedAfter'] = published_after
            if published_before:
                params['publishedBefore'] = published_before
            
            request = self.youtube.search().list(**params)
            return request.execute()
        except HttpError as e:
            if e.resp.status == 403:
                raise Exception("API quota exceeded or invalid API key")
            raise Exception(f"Search request failed: {str(e)}")
    
    def get_video_details(self, video_ids: list) -> Dict[str, Any]:
        """
        Get detailed information for videos
        
        Args:
            video_ids: List of video IDs (max 50)
            
        Returns:
            API response with video statistics
        """
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            return request.execute()
        except HttpError as e:
            raise Exception(f"Video details request failed: {str(e)}")
    
    def get_trending_videos(self, category_id: str = '28', 
                          region_code: str = 'US',
                          max_results: int = 50) -> Dict[str, Any]:
        """
        Get trending videos
        
        Args:
            category_id: Category ID (28 = Science & Technology)
            region_code: Region code
            max_results: Maximum results
            
        Returns:
            API response dictionary
        """
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics',
                chart='mostPopular',
                regionCode=region_code,
                videoCategoryId=category_id,
                maxResults=max_results
            )
            return request.execute()
        except HttpError as e:
            raise Exception(f"Trending videos request failed: {str(e)}")