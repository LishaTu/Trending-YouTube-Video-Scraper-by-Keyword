# Trending YouTube Video Scraper by Keyword

This project is a customizable scraper for trending YouTube videos based on specific keywords. The goal is to extract trending video data by defining these keywords using the YouTube Data API, which allows access to various resources from YouTube.

This project is inspired by [Trending-YouTube-Scraper_Science](https://github.com/LishaTu/Trending-YouTube-Scraper_Science) by mitchelljy. For detailed explanations on using the API and its parameters, refer to the [YouTube Data API documentation](https://developers.google.com/youtube/v3/docs). Additionally, you can find numerous YouTube tutorials that guide you through obtaining and utilizing the API for data scraping.

## About the Keyword Search Method

The keywords are joined as string and defined as the value of the parameter `q` in the [Search list of YouTube](https://developers.google.com/youtube/v3/docs/search/list) to search for the target videos.

It’s worth noting that YouTube’s exact, behind-the-scenes ranking and query parsing are proprietary and evolve over time. Here is a practical, evidence-based summary of how the search query parameter may commonly behave and which video fields it tends to influence.

The query parameter you pass to YouTube search (often via a URL like https://www.youtube.com/results?search_query=...) is the user-visible search term. On the client side, YouTube runs a search over its indexed video data, then ranks results using a complex ranking algorithm (not publicly documented in full).

**What fields are searched**

- **Video title**: Titles are a primary factor. Many search ranking signals are derived from the title text.

- **Video description**: Descriptions are indexed and used. Keywords and content found in descriptions can influence relevance.

- **Tags/Keywords**: YouTube often uses video tags (if provided by the uploader) as part of indexing signals. Tags can help associate a video with related queries.

- **Captions/auto-generated transcripts**: If transcripts or captions exist (manually uploaded or auto-generated), their content can be indexed and influence search relevance.

- **Video metadata**: Channel name and description and video category and other metadata fields (e.g., publish date, duration, number of views, engagement signals)

- **Engagement signals**: While not strictly text fields, metrics like watch time, CTR (click-through rate from the search results), likes/dislikes, comments, and retention can affect ranking but are not direct matches for q terms.

- **Other signals**: Thumbnails, localization data (language/region), and user personalization/history can influence which results appear higher for a given user.

---

## Prerequisites: YouTube Data API

To use the YouTube Data API, follow these steps to create your API key:

1. **Create a Project in Google Cloud**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.

2. **Enable YouTube Data API**:
   - Search for "YouTube Data API" in the API library and enable it.

3. **Create Credentials**:
   - Generate credentials and create an **API key**.
   - Save this key in a text file named `api_key.txt`.

Google Cloud offers a free quota of 10,000 queries per day for the API, with one query returning a maximum of 50 results. The `maxResults` parameter per query (default is `5`) is set to `50`. Please keep an eye on your quota usage; you can view the usage in the `Enabled APIs & Services` section of the Google Cloud Console.

---

## Key Steps in the Scraping Process

The scraping process consists of the following key steps, each represented by a corresponding Python file for easy maintenance and troubleshooting:

1. **Configure API Parameters**: `config_handler.py`

2. **Create YouTube API Wrapper**: `youtube_client.py`

3. **Data Processing Scripts**: `data_processor.py`

4. **Data Storage Functionality**: `storage_handler.py`

5. **Search Logic and Query Management**: `search_handler.py`

6. **Integrate All Components**: `main.py`

For each step, there is a corresponding python file for easy maintenance and trouble shooting. 

---

## Settings and Implementation

The default settings for the scraper are as follows:

- **maxResults**: 50 (maximum number of results per query)

- **region_code**: 'US' (default region)

- **category_id**: setting the value for the `videoCategoryId` parameter of YouTube video, 28 in default (28 = Science & Technology)

- **Output Order**: Results are ordered by view count in descending order.

These settings can be modified directly in the Python scripts as needed.



### Running the Python Files

To run the Python scripts, follow these steps:

```bash
# Create the API key file (replace with your actual API key)
echo "YOUR_YOUTUBE_API_KEY" > api_key.txt

# Install required dependencies
pip install -r requirements.txt

# Start with API key management
python config_handler.py  

# Add YouTube API wrapper
python youtube_client.py

# Create data processing utilities
python data_processor.py

# Add storage functionality
python storage_handler.py

# Implement search logic
python search_handler.py

# Tie everything together
python main.py --keywords space science
```


### Output Formats

The output file can be stored in various formats, including CSV, JSON, and Excel. The output file will be named based on the timestamp of its creation.



### Custom Parameters

You can customize your search using the following parameters:

`api-key-file`: Path to API key file (default: api_key.txt)

`keywords`: Keywords to search, separated by | (OR) and - (NOT).

`max-total-results`: Maximum number of results to fetch (default: 100).

`min-views`: Minimum view count filter (default: 10000)

`order`: Sort order for search results (default: viewCount)

`published_after`: RFC 3339 formatted date-time (e.g., '2024-01-01T00:00:00Z').

`published_before`: RFC 3339 formatted date-time.

`last-days`: Get videos from the last N days.

`date-range`: Specify a date range with start and end dates (two dates in YYYY-MM-DD format).

`output-format`: Output format(s) (default: csv)


**Supported Date Formats are**:

Standard: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS

Relative: today, yesterday, week_ago, month_ago, year_ago



### Example Queries

Here are some example queries you can use to personalize your search:

```bash
# Search for space and science videos
python main.py --keywords space science

# Search with custom parameters, setting the threshold of minimul 50,000 views and output 200 records
python main.py --keywords astronomy physics --max-total-results 200 --min-views 50000

# Get top 50 trending Science & Technology videos 
python main.py --trending --max-total-results 50

# Save output in multiple formats
python main.py --keywords "black hole" --output-format csv json excel

# Use a different API key file
python main.py --api-key-file /path/to/your/api_key.txt --keywords robotics

# Videos from the last 7 days
python main.py --keywords "space exploration" --last-days 7

# Videos published after a specific date
python main.py --keywords "mars rover" --published-after 2024-01-01

# Videos published before a specific date
python main.py --keywords "astronomy" --published-before 2024-12-31

# Videos within a date range
python main.py --keywords "science news" --date-range 2024-06-01 2024-12-31

# Using relative dates
python main.py --keywords "physics" --published-after week_ago

# Combine with other filters
python main.py --keywords "quantum computing" --last-days 30 --min-views 50000

```

### Output

**One record in a sample `csv` output**:

| video_id      | title                  | channel       | published_at          | view_count | like_count | comment_count | duration  | tags      | thumbnail_url                                            | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | url                                          |
|---------------|------------------------|---------------|-----------------------|------------|------------|----------------|-----------|-----------|---------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| BYVZh5kqaFg   | Egg Drop From Space     | Mark Rober    | 2022-11-25T14:59:03Z | 137775274  | 2024435    | 40550          | PT26M57S  | No tags   | https://i.ytimg.com/vi/BYVZh5kqaFg/hqdefault.jpg    | Next year we’re doing this on Mars. Ask for the CrunchLabs Build Box for Christmas ... | https://www.youtube.com/watch?v=BYVZh5kqaFg |


**One record in a sample `json` output***:

 "timestamp": "2025-09-19T14:37:17.052520",
  "video_count": 286,
  "videos": [
    {
      "video_id": "BYVZh5kqaFg",
      "title": "Egg Drop From Space",
      "channel": "Mark Rober",
      "channel_id": "UCY1kMZp36IQSyNx_9h4mpCg",
      "published_at": "2022-11-25T14:59:03Z",
      "description": "Next year we’re doing this on Mars ...",
      "description_short": "Next year we’re doing this on Mars ... ",
      "view_count": 137775274,
      "like_count": 2024435,
      "comment_count": 40550,
      "duration": "PT26M57S",
      "tags": "No tags",
      "tags_list": [],
      "url": "https://www.youtube.com/watch?v=BYVZh5kqaFg",
      "thumbnail": {
        "url": "https://i.ytimg.com/vi/BYVZh5kqaFg/hqdefault.jpg",
        "width": 480,
        "height": 360
      }
