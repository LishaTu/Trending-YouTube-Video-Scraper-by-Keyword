"""
Data processor for YouTube video data
Filters, sorts, and formats video information
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class DataProcessor:
    """Processes and filters YouTube video data"""
    
    @staticmethod
    def extract_video_info(video: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant information from video data
        
        Args:
            video: Raw video data from API
            
        Returns:
            Processed video information
        """
        snippet = video.get('snippet', {})
        statistics = video.get('statistics', {})
        
        # Parse view count (convert to int, default to 0 if missing)
        view_count = int(statistics.get('viewCount', 0))
        
        # Parse duration (if available)
        duration = video.get('contentDetails', {}).get('duration', 'N/A')
        
        # Extract tags - join them as comma-separated string
        tags = snippet.get('tags', [])
        tags_string = ', '.join(tags) if tags else 'No tags'

        return {
            'video_id': video.get('id'),
            'title': snippet.get('title', ''),
            'channel': snippet.get('channelTitle', ''),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt', ''),
            'description': snippet.get('description', '')[:500],  # First 500 chars
            'view_count': view_count,
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'duration': duration,
            'tags': tags_string,  # Added tags field
            'tags_list': tags,    # Keep original list for filtering
            'url': f"https://www.youtube.com/watch?v={video.get('id')}",
            'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
        }
    
    @staticmethod
    def filter_by_views(videos: List[Dict[str, Any]], 
                       min_views: int = 10000) -> List[Dict[str, Any]]:
        """
        Filter videos by minimum view count
        
        Args:
            videos: List of video data
            min_views: Minimum view count threshold
            
        Returns:
            Filtered list of videos
        """
        return [v for v in videos if v.get('view_count', 0) >= min_views]
    
    @staticmethod
    def filter_by_keywords_in_title(videos: List[Dict[str, Any]], 
                                  keywords: List[str],
                                  case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Filter videos that contain keywords in title
        
        Args:
            videos: List of video data
            keywords: Keywords to search for
            case_sensitive: Whether to use case-sensitive matching
            
        Returns:
            Filtered list of videos
        """
        filtered = []
        
        for video in videos:
            title = video.get('title', '')
            if not case_sensitive:
                title = title.lower()
                keywords = [k.lower() for k in keywords]
            
            if any(keyword in title for keyword in keywords):
                filtered.append(video)
        
        return filtered
    
    @staticmethod
    def sort_videos(videos: List[Dict[str, Any]], 
                   sort_by: str = 'view_count',
                   descending: bool = True) -> List[Dict[str, Any]]:
        """
        Sort videos by specified field
        
        Args:
            videos: List of video data
            sort_by: Field to sort by
            descending: Sort order
            
        Returns:
            Sorted list of videos
        """
        return sorted(
            videos, 
            key=lambda x: x.get(sort_by, 0), 
            reverse=descending
        )
    
    @staticmethod
    def process_video_batch(raw_videos: List[Dict[str, Any]],
                          min_views: int = 10000,
                          filter_keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Process a batch of raw video data
        
        Args:
            raw_videos: Raw video data from API
            min_views: Minimum view count
            filter_keywords: Keywords to filter by
            
        Returns:
            Processed and filtered videos
        """
        # Extract video information
        processed = [DataProcessor.extract_video_info(v) for v in raw_videos]
        
        # Filter by views
        processed = DataProcessor.filter_by_views(processed, min_views)
        
        # Filter by keywords if provided
        if filter_keywords:
            processed = DataProcessor.filter_by_keywords_in_title(
                processed, filter_keywords
            )
        
        # Sort by view count
        processed = DataProcessor.sort_videos(processed)
        
        return processed
