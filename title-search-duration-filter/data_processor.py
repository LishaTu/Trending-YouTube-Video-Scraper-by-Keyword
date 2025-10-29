"""
Data processor for YouTube video data
Filters, sorts, and formats video information
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class DataProcessor:
    """Processes and filters YouTube video data"""
    
    # --- This part is added for duration parsing and filtering ---
    # Parses ISO 8601 duration format, categorizes videos, and filters by duration
    # This part is added in version 3
    @staticmethod
    def parse_duration(duration_str: str) -> int:
        """
        Parse YouTube ISO 8601 duration format to seconds
        
        Args:
            duration_str: Duration in ISO 8601 format (e.g., 'PT4M13S', 'PT1H2M10S', 'PT45S')
            
        Returns:
            Duration in seconds
        """
        if not duration_str or duration_str == 'N/A':
            return 0
            
        # Remove PT prefix
        duration_str = duration_str.replace('PT', '')
        
        # Parse hours, minutes, seconds
        hours = 0
        minutes = 0
        seconds = 0
        
        # Extract hours
        hours_match = re.search(r'(\d+)H', duration_str)
        if hours_match:
            hours = int(hours_match.group(1))
            
        # Extract minutes
        minutes_match = re.search(r'(\d+)M', duration_str)
        if minutes_match:
            minutes = int(minutes_match.group(1))
            
        # Extract seconds
        seconds_match = re.search(r'(\d+)S', duration_str)
        if seconds_match:
            seconds = int(seconds_match.group(1))
            
        return hours * 3600 + minutes * 60 + seconds
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """
        Format duration in seconds to human-readable string
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string (e.g., "1:02:30" or "0:45")
        """
        if seconds == 0:
            return "0:00"
            
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    @staticmethod
    def is_youtube_short(duration_seconds: int) -> bool:
        """
        Determine if a video is a YouTube Short based on duration
        
        Args:
            duration_seconds: Video duration in seconds
            
        Returns:
            True if video is a Short (≤60 seconds), False otherwise
        """
        return 0 < duration_seconds <= 60
    
    @staticmethod
    def get_video_type(duration_seconds: int) -> str:
        """
        Categorize video by duration
        
        Args:
            duration_seconds: Video duration in seconds
            
        Returns:
            Video type category
        """
        if duration_seconds == 0:
            return "Unknown"
        elif duration_seconds <= 60:
            return "Short"
        elif duration_seconds <= 240:  # 4 minutes
            return "Short Video"
        elif duration_seconds <= 600:  # 10 minutes
            return "Medium Video"
        elif duration_seconds <= 1200:  # 20 minutes
            return "Long Video"
        else:
            return "Very Long Video"
    


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
        content_details = video.get('contentDetails', {})
    
        # Parse view count (convert to int, default to 0 if missing)
        view_count = int(statistics.get('viewCount', 0))
    
        # Parse duration
        # This part is modified in version 3
        duration_iso = content_details.get('duration', 'N/A')
        duration_seconds = DataProcessor.parse_duration(duration_iso)
        duration_formatted = DataProcessor.format_duration(duration_seconds)

        # Determine if it's a YouTube Short
        is_short = DataProcessor.is_youtube_short(duration_seconds)
        video_type = DataProcessor.get_video_type(duration_seconds)
    
        # Extract tags - join them as comma-separated string
        tags = snippet.get('tags', [])
        tags_string = ', '.join(tags) if tags else 'No tags'
    
        # Extract thumbnail object (high quality)
        thumbnail_high = snippet.get('thumbnails', {}).get('high', {})
        thumbnail_info = {
            'url': thumbnail_high.get('url', ''),
            'width': thumbnail_high.get('width', 0),
            'height': thumbnail_high.get('height', 0)
        }
    
        # Format thumbnail as string for CSV/Excel
        thumbnail_string = thumbnail_info['url'] if thumbnail_info['url'] else 'No thumbnail'
    
        # Get full description
        full_description = snippet.get('description', '')
    
        return {
            'video_id': video.get('id'),
            'title': snippet.get('title', ''),
            'channel': snippet.get('channelTitle', ''),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt', ''),
            'description': full_description,  # Full description
            'description_short': full_description[:500],  # First 500 chars
            'view_count': view_count,
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'duration': duration_formatted,  # Human-readable format
            'duration_seconds': duration_seconds,  # Numeric value for filtering
            'is_short': is_short,  # Boolean: True if ≤60 seconds
            'video_type': video_type,  # Category: Short, Medium, Long, etc.
            'tags': tags_string,
            'tags_list': tags,
            'thumbnail_url': thumbnail_string,  # Just URL for CSV
            'thumbnail_object': thumbnail_info,  # Full object for JSON
            'url': f"https://www.youtube.com/watch?v={video.get('id')}"
        }
    
    # --- This part is modified for filtering video duration ---
    @staticmethod
    def filter_by_video_type(videos: List[Dict[str, Any]], 
                           video_types: List[str]) -> List[Dict[str, Any]]:
        """
        Filter videos by type (Short, Medium, Long, etc.)
        
        Args:
            videos: List of video data
            video_types: List of video types to include
            
        Returns:
            Filtered list of videos
        """
        return [v for v in videos if v.get('video_type') in video_types]
    
    @staticmethod
    def filter_shorts_only(videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter to get only YouTube Shorts
        
        Args:
            videos: List of video data
            
        Returns:
            List of YouTube Shorts only
        """
        return [v for v in videos if v.get('is_short', False)]
    
    @staticmethod
    def filter_regular_videos_only(videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter to exclude YouTube Shorts
        
        Args:
            videos: List of video data
            
        Returns:
            List of regular videos (non-Shorts)
        """
        return [v for v in videos if not v.get('is_short', False)]
    
    @staticmethod
    def filter_by_duration(videos: List[Dict[str, Any]], 
                         min_seconds: int = 0,
                         max_seconds: int = float('inf')) -> List[Dict[str, Any]]:
        """
        Filter videos by duration range
        
        Args:
            videos: List of video data
            min_seconds: Minimum duration in seconds
            max_seconds: Maximum duration in seconds
            
        Returns:
            Filtered list of videos
        """
        return [v for v in videos 
                if min_seconds <= v.get('duration_seconds', 0) <= max_seconds]
    
    # --- End of duration parsing and filtering part ---

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