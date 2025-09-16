# Trending YouTube Video Scraper by Keyword

This project is a customizable scraper for trending YouTube videos based on specific keywords. The goal is to extract trending video data by defining these keywords using the YouTube Data API, which allows access to various resources from YouTube.

This project is inspired by [Trending-YouTube-Scraper_Science](https://github.com/LishaTu/Trending-YouTube-Scraper_Science) by mitchelljy. For detailed explanations on using the API and its parameters, refer to the [YouTube Data API documentation](https://developers.google.com/youtube/v3/docs). Additionally, you can find numerous YouTube tutorials that guide you through obtaining and utilizing the API for data scraping.

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

`keywords`: Keywords to search, separated by | (OR) and - (NOT).

`max_total_results`: Maximum total results to fetch.

`published_after`: RFC 3339 formatted date-time (e.g., '2024-01-01T00:00:00Z').

`published_before`: RFC 3339 formatted date-time.

`last-days`: Get videos from the last N days.

`date-range`: Specify a date range with start and end dates.

Supported Date Formats are:

Standard: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS

Relative: today, yesterday, week_ago, month_ago, year_ago

