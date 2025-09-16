"""
Main script for YouTube Data Scraper
Command-line interface for searching and downloading YouTube video data
"""
import argparse
import sys
from typing import List, Optional
from datetime import datetime, timedelta
from config_handler import ConfigHandler
from youtube_client import YouTubeClient
from search_handler import SearchHandler
from data_processor import DataProcessor
from storage_handler import StorageHandler


def parse_date_string(date_str: str) -> str:
    """
    Parse date string and convert to RFC 3339 format
    
    Accepts formats:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM:SS
    - 'today', 'yesterday', 'week_ago', 'month_ago', 'year_ago'
    
    Args:
        date_str: Date string to parse
        
    Returns:
        RFC 3339 formatted date-time string
    """
    # Handle relative dates
    now = datetime.now()
    relative_dates = {
        'today': now,
        'yesterday': now - timedelta(days=1),
        'week_ago': now - timedelta(weeks=1),
        'month_ago': now - timedelta(days=30),
        'year_ago': now - timedelta(days=365),
    }
    
    if date_str.lower() in relative_dates:
        dt = relative_dates[date_str.lower()]
    else:
        # Try parsing different date formats
        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']:
            try:
                dt = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Invalid date format: {date_str}")
    
    # Convert to RFC 3339 format (YouTube API requirement)
    return dt.isoformat() + 'Z'


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='YouTube Data Scraper - Search and download video information'
    )
    
    # Required arguments
    parser.add_argument(
        '--api-key-file',
        type=str,
        default='api_key.txt',
        help='Path to API key file (default: api_key.txt)'
    )
    
    # Search parameters
    parser.add_argument(
        '--keywords',
        type=str,
        nargs='+',
        default=['space', 'science'],
        help='Keywords to search for (default: space science)'
    )
    
    parser.add_argument(
        '--max-results',
        type=int,
        default=100,
        help='Maximum number of results to fetch (default: 100)'
    )
    
    parser.add_argument(
        '--min-views',
        type=int,
        default=10000,
        help='Minimum view count filter (default: 10000)'
    )
    
    parser.add_argument(
        '--order',
        type=str,
        choices=['viewCount', 'relevance', 'date', 'rating', 'title'],
        default='viewCount',
        help='Sort order for search results (default: viewCount)'
    )
    
    # Date filtering arguments - NEW
    parser.add_argument(
        '--published-after',
        type=str,
        help='Only videos published after this date (YYYY-MM-DD or relative: today, yesterday, week_ago, month_ago, year_ago)'
    )
    
    parser.add_argument(
        '--published-before',
        type=str,
        help='Only videos published before this date (YYYY-MM-DD or relative)'
    )
    
    parser.add_argument(
        '--last-days',
        type=int,
        help='Shortcut for videos from last N days'
    )
    
    parser.add_argument(
        '--date-range',
        type=str,
        nargs=2,
        metavar=('START', 'END'),
        help='Date range for videos (two dates in YYYY-MM-DD format)'
    )
    
    # Output options
    parser.add_argument(
        '--output-format',
        type=str,
        nargs='+',
        choices=['csv', 'json', 'excel'],
        default=['csv'],
        help='Output format(s) (default: csv)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    # Other options
    parser.add_argument(
        '--trending',
        action='store_true',
        help='Fetch trending videos instead of search'
    )
    
    parser.add_argument(
        '--estimate-quota',
        action='store_true',
        help='Estimate API quota usage before running'
    )
    
    return parser.parse_args()


def main():
    """Main execution function"""
    # Parse arguments
    args = parse_arguments()
    
    print("YouTube Data Scraper")
    print("=" * 50)
    
    # Process date arguments
    published_after = None
    published_before = None
    
    try:
        # Handle different date input methods
        if args.last_days:
            # Videos from last N days
            published_after = parse_date_string(
                (datetime.now() - timedelta(days=args.last_days)).strftime('%Y-%m-%d')
            )
        elif args.date_range:
            # Specific date range
            published_after = parse_date_string(args.date_range[0])
            published_before = parse_date_string(args.date_range[1])
        else:
            # Individual date filters
            if args.published_after:
                published_after = parse_date_string(args.published_after)
            if args.published_before:
                published_before = parse_date_string(args.published_before)
    except ValueError as e:
        print(f"❌ Date parsing error: {e}")
        sys.exit(1)
    
    try:
        # Initialize configuration
        print(f"Loading API key from: {args.api_key_file}")
        config = ConfigHandler(args.api_key_file)
        api_key = config.load_api_key()
        print("✓ API key loaded successfully")
        
        # Estimate quota usage
        if args.estimate_quota:
            # Rough estimate: 1 search per 50 results + 1 detail request per 50 videos
            num_searches = (args.max_results // 50) + 1
            quota = config.estimate_quota_usage(num_searches, args.max_results)
            print(f"\nEstimated quota usage: {quota} units")
            response = input("Continue? (y/n): ")
            if response.lower() != 'y':
                print("Aborted by user")
                return
        
        # Initialize YouTube client
        print("\nInitializing YouTube client...")
        youtube_client = YouTubeClient(api_key)
        print("✓ Client initialized")
        
        # Initialize handlers
        search_handler = SearchHandler(youtube_client)
        storage_handler = StorageHandler(args.output_dir)
        
        # Fetch videos
        if args.trending:
            print("\nFetching trending Science & Technology videos...")
            response = youtube_client.get_trending_videos(
                category_id='28',  # Science & Technology
                max_results=min(args.max_results, 50)
            )
            raw_videos = response.get('items', [])
            print(f"✓ Found {len(raw_videos)} trending videos")
        else:
            print(f"\nSearching for: {' '.join(args.keywords)}")
            print(f"Order by: {args.order}")
            print(f"Max results: {args.max_results}")
            if published_after:
                print(f"Published after: {published_after}")
            if published_before:
                print(f"Published before: {published_before}")
            
            raw_videos = search_handler.search_and_get_details(
                keywords=args.keywords,
                max_results=args.max_results,
                published_after=published_after,
                published_before=published_before
            )
            print(f"✓ Found {len(raw_videos)} videos total")
        
        # Process videos
        print("\nProcessing videos...")
        processed_videos = DataProcessor.process_video_batch(
            raw_videos,
            min_views=args.min_views,
            filter_keywords=args.keywords if not args.trending else None
        )
        print(f"✓ {len(processed_videos)} videos after filtering (min views: {args.min_views})")
        
        if not processed_videos:
            print("\nNo videos found matching criteria!")
            return
        
        # Display top 10 results
        print("\nTop 10 videos by view count:")
        print("-" * 50)
        for i, video in enumerate(processed_videos[:10], 1):
            print(f"{i}. {video['title']}")
            print(f"   Views: {video['view_count']:,}")
            print(f"   Channel: {video['channel']}")
            print(f"   Tags: {video['tags'][:100]}...")  # Show first 100 chars of tags
            print(f"   URL: {video['url']}")
            print()
        
        # Save results
        print("Saving results...")
        saved_files = []
        
        if 'csv' in args.output_format:
            filepath = storage_handler.save_to_csv(
                processed_videos, 
                f"youtube_{args.keywords[0]}"
            )
            saved_files.append(filepath)
        
        if 'json' in args.output_format:
            filepath = storage_handler.save_to_json(
                processed_videos,
                f"youtube_{args.keywords[0]}"
            )
            saved_files.append(filepath)
        
        if 'excel' in args.output_format:
            filepath = storage_handler.save_to_excel(
                processed_videos,
                f"youtube_{args.keywords[0]}"
            )
            saved_files.append(filepath)
        
        print("\n✓ Complete! Files saved:")
        for filepath in saved_files:
            print(f"  - {filepath}")
        
        # Summary statistics
        print(f"\nSummary:")
        print(f"  Total videos: {len(processed_videos)}")
        print(f"  Total views: {sum(v['view_count'] for v in processed_videos):,}")
        print(f"  Average views: {sum(v['view_count'] for v in processed_videos) // len(processed_videos):,}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create an 'api_key.txt' file with your YouTube API key.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()