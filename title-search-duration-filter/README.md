## Key Updates:

This folder includes files for running a title search model (searching keywords only in title) with added functions to filter video durations. 

**Videos are classified as**:

- **`is_short`**: Boolean field - `True` if video is ≤60 seconds (YouTube Short)

- **`video_type`**: Categories based on duration:
    - Short (≤60s)
    - Short Video (1-4 min)
    - Medium Video (4-10 min)
    - Long Video (10-20 min)
    - Very Long Video (>20 min)

**The output columns added**: 

- `duration`: Human-readable (e.g., "0:45", "10:30")
- `duration_seconds`: Numeric value for calculations
- `is_short`: True/False
- `video_type`: Category name

## Sample Use Cases

The `video-type-filter` paramter and the `custom-types` parameter can be customized:

- **`video-type-filter`**: 'all', 'shorts-only', 'no-shorts', 'custom'

- **`custom-types`**: 'Short', 'Short Video', 'Medium Video', 'Long Video', 'Very Long Video'

Here are the definition of the two parameters:
```python
 # Add video type filtering arguments
    parser.add_argument(
        '--video-type-filter',
        type=str,
        choices=['all', 'shorts-only', 'no-shorts', 'custom'],
        default='all',
        help='Filter videos by type: all, shorts-only, no-shorts, or custom (default: all)'
    )
    
    parser.add_argument(
        '--custom-types',
        type=str,
        nargs='+',
        choices=['Short', 'Short Video', 'Medium Video', 'Long Video', 'Very Long Video'],
        help='When using --video-type-filter custom, specify which types to include'
    )
```

Here are some sample queries:
```python
# Analyze only viral Shorts
python main.py --keywords "viral" --video-type-filter shorts-only --min-views 1000000

# Find long-form educational content
python main.py --keywords "lecture" --video-type-filter custom --custom-types "Long Video" "Very Long Video"

# Get medium-length tutorials from last month
python main.py --keywords "python tutorial" --duration-min 240 --duration-max 1200 --last-days 30
```

