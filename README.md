# YouTube Scam Video Crawler

A Python-based web scraping tool designed to identify and collect YouTube Shorts videos that exhibit characteristics of common scam types including crypto scams, gift card generator scams, and fake giveaways.

## Features

- 🔍 **Multi-category scam detection**: Crypto, gift card generators, and giveaway scams
- 🎯 **Intelligent filtering**: View count limits and duration checks
- 📊 **Comprehensive metadata extraction**: Title, description, tags, engagement metrics
- 💾 **Automated video downloading**: Optional MP4 downloads
- 🔄 **Smart crawling**: Recursive channel exploration for efficient data collection
- 📝 **Structured JSON output**: Organized metadata storage

## Scam Categories

### 1. Crypto Scams (`video_crawler_crypto.py`)
Targets videos promoting:
- Free Bitcoin/cryptocurrency giveaways
- Crypto doublers and generators
- Celebrity impersonation (e.g., "Elon Musk giveaway")
- Guaranteed returns and investment scams
- Fake airdrops and mining offers

### 2. Gift Card Scams (`video_crawler_giftcards.py`)
Targets videos promoting:
- Free gift card generators (PSN, Xbox, Steam, etc.)
- Unlimited code generators
- Fake redemption websites
- "Working" gift card hacks

### 3. Giveaway Scams (`video_crawler_giveaway.py`)
Targets videos promoting:
- Free iPhone/PS5/electronics giveaways
- Cash giveaways (PayPal, Venmo, CashApp)
- "Guaranteed winner" schemes
- Fake influencer giveaways

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Windows OS (path configurations are Windows-specific)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-scam-crawler.git
cd youtube-scam-crawler
```

### 2. Install Required Dependencies

```bash
pip install yt-dlp selenium webdriver-manager
```

**Required packages:**
- `yt-dlp` - YouTube video downloader and metadata extractor
- `selenium` - Web browser automation
- `webdriver-manager` - Automatic ChromeDriver management

### 3. Configure Output Directory

Edit the `OUTPUT_DIR` variable in each script to match your desired output location:

```python
OUTPUT_DIR = r"C:\Users\YourUsername\Desktop\video_crawler"
```

## Configuration

Each script contains configurable parameters at the top:

```python
OUTPUT_DIR = r"C:\Users\Jules Gregory\Desktop\video_crawler"  # Output directory
MAX_VIDEOS = 5                    # Maximum videos to collect
SCROLL_ROUNDS = 8                 # Number of scroll iterations per search
DOWNLOAD_VIDEOS = True            # Enable/disable video downloading
MAX_VIEW_COUNT = 30000            # Skip videos exceeding this view count
```

### Recommended Settings

**For testing:**
```python
MAX_VIDEOS = 5-10
SCROLL_ROUNDS = 8
DOWNLOAD_VIDEOS = True
```

**For production data collection:**
```python
MAX_VIDEOS = 2000
SCROLL_ROUNDS = 15-20
DOWNLOAD_VIDEOS = True  # Requires significant storage
```

## Usage

### Running a Crawler

Execute any of the three crawlers:

```bash
# Crypto scam crawler
python video_crawler_crypto.py

# Gift card scam crawler
python video_crawler_giftcards.py

# Giveaway scam crawler
python video_crawler_giveaway.py
```

### What Happens During Execution

1. **Chrome Browser Launch**: Selenium opens an automated Chrome window
2. **Search Query Execution**: Iterates through predefined search queries
3. **Page Scrolling**: Scrolls multiple times to load more Shorts
4. **Video Discovery**: Extracts video links from search results
5. **Metadata Extraction**: Uses yt-dlp to fetch video information
6. **Filtering**: Applies keyword detection and view count filters
7. **Data Saving**: Stores metadata as JSON files
8. **Video Download**: (Optional) Downloads matching videos as MP4 files
9. **Channel Crawling**: Recursively explores channels of scam videos

### Output Structure

```
video_crawler/
├── metadata/
│   ├── youtube_shorts_crypto/
│   │   ├── youtube_VIDEO_ID_1.json
│   │   └── youtube_VIDEO_ID_2.json
│   ├── youtube_shorts_giftcard/
│   │   └── ...
│   └── youtube_shorts_giveaway/
│       └── ...
└── videos/
    ├── youtube_shorts_crypto/
    │   ├── youtube_VIDEO_ID_1.mp4
    │   └── youtube_VIDEO_ID_2.mp4
    ├── youtube_shorts_giftcard/
    │   └── ...
    └── youtube_shorts_giveaway/
        └── ...
```

### Metadata JSON Format

Each video generates a JSON file with the following structure:

```json
{
  "video_id": "youtube_ABC123XYZ",
  "platform": "youtube",
  "video_url": "https://www.youtube.com/shorts/ABC123XYZ",
  "title": "Video Title",
  "description": "Video description...",
  "uploader": "Channel Name",
  "channel": "Channel Name",
  "upload_date": "20240115",
  "duration": 45,
  "view_count": 15000,
  "like_count": 500,
  "comment_count": 120,
  "tags": ["tag1", "tag2"],
  "hashtags": ["#scam", "#free"],
  "is_short": true,
  "label": "Scam",
  "scam_type": "Crypto Scam",
  "scraped_at": "2024-01-15 14:30:00",
  "scraper_id": "COMPUTER-NAME"
}
```

## Customization

### Adding Custom Search Queries

Edit the `SEARCH_QUERIES` list in any script:

```python
SEARCH_QUERIES = [
    "your custom query",
    "another search term",
    # ... more queries
]
```

### Modifying Keyword Detection

Update the keyword lists to refine scam detection:

```python
CRYPTO_SCAM_KEYWORDS = [
    "bitcoin",
    "free crypto",
    # ... add your keywords
]
```

### Running in Headless Mode

Uncomment the headless option in `setup_driver()`:

```python
options.add_argument("--headless")  # Runs Chrome without GUI
```

## Interrupting Execution

Press `Ctrl+C` at any time to gracefully stop the crawler. The script will:
- Close the Chrome browser
- Display final statistics
- Preserve all collected data

## Troubleshooting

### Common Issues

**ChromeDriver Issues:**
- The script automatically downloads the correct ChromeDriver version
- If issues persist, manually update Chrome browser

**Rate Limiting:**
- YouTube may temporarily block requests if crawling too aggressively
- Increase sleep intervals: `time.sleep(random.uniform(3, 7))`

**Memory Issues:**
- Reduce `MAX_VIDEOS` for large collection runs
- Disable video downloading: `DOWNLOAD_VIDEOS = False`

**Encoding Errors:**
- Scripts use UTF-8 encoding by default
- Windows users: ensure console supports UTF-8 or redirect output

## Ethical Considerations

⚠️ **Important Notice:**

- This tool is designed for **research and educational purposes**
- Respect YouTube's Terms of Service and robots.txt
- Implement appropriate rate limiting
- Do not use collected data to harm or harass content creators
- Consider the ethical implications of automated scraping

## Legal Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring their use complies with:
- YouTube's Terms of Service
- Applicable copyright laws
- Data protection regulations (GDPR, CCPA, etc.)
- Local laws regarding web scraping

The authors assume no liability for misuse of this software.

## Performance Notes

- **Speed**: ~2-5 videos per minute (depending on network and configuration)
- **Storage**: Each video ~5-30MB; metadata ~2-5KB per video
- **Network**: Moderate bandwidth usage; respectful delays implemented

## Future Improvements

- [ ] Multi-platform support (TikTok, Instagram Reels)
- [ ] Machine learning-based scam classification
- [ ] Database integration (MongoDB, PostgreSQL)
- [ ] Web dashboard for data visualization
- [ ] Proxy support for distributed crawling
- [ ] Resume functionality for interrupted runs

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

For questions, issues, or collaboration:
- Open an issue on GitHub
- Email: your.email@example.com

---

**Disclaimer**: This tool identifies potential scam content based on keyword patterns. Not all flagged content is necessarily fraudulent, and manual review is recommended for research purposes.
