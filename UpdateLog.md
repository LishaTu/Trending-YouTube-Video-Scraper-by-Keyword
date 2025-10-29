# Script Update and Output
### Second Update: 18, Sep. 
Extract thumbnail object and full description from the `snippet` parameter ([YouTube Data API | Videos: list](https://developers.google.com/youtube/v3/docs/videos/list?hl=en)). Two columns `thumbnail_url` and `description` are added to the output

### Third Update: 24, Sep.
#### Script Update
First, we have discussed to filter videos by categoryId to improve the accuracy and relevance of video searching. This parameter, referring to `videoCategoryId` ([YouTube Data API | Search: list](https://developers.google.com/youtube/v3/docs/search/list?hl=en)), is then updated and set to be 28 (Category 28: Science & Technology) by default in the scraping scripts.

I want to explore whether videos can be filtered by the keywords in their title. However, I cannot find a parameter to restrict the search in title. 

The good news is that I've found an unofficially published way to specifically look for title - using the `intitle` search operator which is not recorded in YouTube API documents but found in some online forums. Besides, this method using `intitle` is not official supported, it may stop working without notice or have some potential issues.

**Note**: 
The currently used keyword searching method uses the `q` parameter ([YouTube Data API | Search: list](https://developers.google.com/youtube/v3/docs/search/list?hl=en)) to match the keywords across multiple fields of video (title, description, tags, video metadata, etc.) to fetch the required videos. However, the searching process is driven by a complex ranking algorithm that is not publicly documented yet. That means, we cannot select where the `q` will look into, e.g. title, tag, description. 

#### Query & Output
```
# Find videos with both "space" AND "science" in the title
# setting the max return to be 20,000
# minimal views 10,000, published after 2025

python main_title_only.py --keywords space science --max-total-results 20000 --min-views 10000 --published-after 2025-01-01 --output-format csv
```

Here's the link for the output, edit permission is allowed for anyone: 
https://drive.google.com/file/d/1KgaAZS9lj0TCnb0DlnjO021ct1FpQ-Zo/view?usp=drive_link

Some simple analysis:
- Searching keywords in topic has results that are more closely aligned with those keywords.
- Channels with a high number of subscriptions tend to have more views on their videos. These channels may appear multiple times in the table with high view counts. They consistently update their content and present real science stories about the universe in an engaging and captivating manner.

### Forth Update: 18, Oct.
Add the time duration columns in the output file, the video `duration`, `duration-seconds`, `is_short`, and `video_type` are added. 
A duration filter is also added. Videos can be filtered by their duration type using `video-type-filter`:

- **`video_type`**: Categories based on duration:
    - Short (≤60s)
    - Short Video (1-4 min)
    - Medium Video (4-10 min)
    - Long Video (10-20 min)
    - Very Long Video (>20 min)

A sample query: 'python main.py --keywords "science experiments" --video-type-filter shorts-only' to filter the short videos (≤60s), or 'python main.py --keywords "lecture" --video-type-filter custom --custom-types "Long Video" "Very Long Video"' to filter long and very long videos 

Here are the definition of the `video-type-filter` paramter, and the `custom-types` parameter:

- **`video-type-filter`**: 'all', 'shorts-only', 'no-shorts', 'custom'

- **`custom-types`**: 'Short', 'Short Video', 'Medium Video', 'Long Video', 'Very Long Video'

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
