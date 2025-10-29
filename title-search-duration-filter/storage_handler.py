"""
Storage handler for YouTube data
Saves data to CSV and JSON formats
"""
import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd


class StorageHandler:
    """Handles data storage operations"""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize storage handler
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        self._create_output_dir()
    
    def _create_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _generate_filename(self, base_name: str, extension: str) -> str:
        """
        Generate filename with timestamp
        
        Args:
            base_name: Base name for file
            extension: File extension
            
        Returns:
            Full file path
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{base_name}_{timestamp}.{extension}"
        return os.path.join(self.output_dir, filename)
    
    def save_to_csv(self, videos: List[Dict[str, Any]], 
               filename_base: str = 'youtube_videos') -> str:
        
        """
        Save videos to CSV file
        
        Args:
            videos: List of video data
            filename_base: Base name for file
            
        Returns:
            Path to saved file
        """

        if not videos:
            print("No videos to save")
            return ""
        
        filepath = self._generate_filename(filename_base, 'csv')
        
        # Define CSV columns - UPDATED to include thumbnail and description
        columns = [
            'video_id', 'title', 'channel', 'published_at',
            'view_count', 'like_count', 'comment_count',
            'duration', 'duration_seconds', 'is_short', 'video_type',
            'tags', 'thumbnail_url', 'description', 'url'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            
            for video in videos:
                # Write only specified columns
                row = {col: video.get(col, '') for col in columns}
                writer.writerow(row)
        
        print(f"Saved {len(videos)} videos to: {filepath}")
        return filepath

    def save_to_json(self, videos: List[Dict[str, Any]], 
                     filename_base: str = 'youtube_videos') -> str:
        """
        Save videos to JSON file
        
        Args:
            videos: List of video data
            filename_base: Base name for file
            
        Returns:
            Path to saved file
        """
        if not videos:
            print("No videos to save")
            return ""
        
        filepath = self._generate_filename(filename_base, 'json')
        
        # For JSON, include the full thumbnail object
        videos_with_full_data = []
        for video in videos:
            video_copy = video.copy()
            # Replace thumbnail_url with thumbnail_object for JSON
            if 'thumbnail_object' in video:
                video_copy['thumbnail'] = video['thumbnail_object']
                # Remove redundant fields
                video_copy.pop('thumbnail_url', None)
                video_copy.pop('thumbnail_object', None)
            videos_with_full_data.append(video_copy)
        
        # Add metadata
        data = {
            'timestamp': datetime.now().isoformat(),
            'video_count': len(videos_with_full_data),
            'videos': videos_with_full_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(videos)} videos to: {filepath}")
        return filepath

    def save_to_excel(self, videos: List[Dict[str, Any]], 
                    filename_base: str = 'youtube_videos') -> str:
        """
        Save videos to Excel file
        
        Args:
            videos: List of video data
            filename_base: Base name for file
            
        Returns:
            Path to saved file
        """
        if not videos:
            print("No videos to save")
            return ""
        
        filepath = self._generate_filename(filename_base, 'xlsx')
        
        # Convert to DataFrame
        df = pd.DataFrame(videos)
        
        # Reorder columns - UPDATED to include thumbnail and description
        column_order = [
            'video_id', 'title', 'channel', 'view_count',
            'like_count', 'comment_count', 'published_at',
            'duration', 'duration_seconds', 'is_short', 'video_type',
            'tags', 'thumbnail_url', 'description', 'url'
        ]
        
        # Keep only existing columns in desired order
        columns = [col for col in column_order if col in df.columns]
        df = df[columns]
        
        # Save to Excel with formatting
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='YouTube Videos', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['YouTube Videos']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        cell_value = str(cell.value)
                        # Limit description column width
                        if cell.column == df.columns.get_loc('description') + 1:
                            max_length = min(len(cell_value), 50)
                        else:
                            max_length = max(max_length, len(cell_value))
                    except:
                        pass
                
                # Set maximum width limits
                if column_letter == worksheet.cell(1, df.columns.get_loc('description') + 1).column_letter:
                    adjusted_width = 50  # Fixed width for description
                else:
                    adjusted_width = min(max_length + 2, 50)
                
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Saved {len(videos)} videos to: {filepath}")
        return filepath