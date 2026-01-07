# YouTube Shorts Scam Scraper

A collection of Python-based YouTube Shorts crawlers designed to **discover, classify, and optionally download scam-related Shorts** using Selenium and `yt-dlp`.

This repository includes **three specialized scrapers**:

1. **Crypto Scam Shorts Scraper**
2. **Giveaway Scam Shorts Scraper**
3. **Gift Card / Code Generator Scam Shorts Scraper**

Each scraper:

- Discovers Shorts via YouTube search
- Filters videos by duration (≤ 60 seconds)
- Filters videos by view count
- Uses keyword heuristics to label scam content
- Saves structured JSON metadata
- Optionally downloads the video file

---

## ⚠️ Legal & Ethical Notice

This project is for **research, academic, security, and anti-fraud purposes only**.

- Do **not** harass or target creators  
- Respect YouTube’s Terms of Service  
- Use collected data responsibly  

You are responsible for how this software is used.

---

## 📁 Repository Structure

```text
video-crawler/
│
├── crypto_scam_scraper.py
├── giveaway_scam_scraper.py
├── giftcard_scam_scraper.py
│
├── requirements.txt
└── README.md
🐍 Python Dependencies & Installation
Create requirements.txt:

txt
Copy code
yt-dlp
selenium
webdriver-manager
Then install dependencies with:

bash
Copy code
pip install -r requirements.txt
No manual ChromeDriver setup is required. webdriver-manager will:

Detect your Chrome version

Download the correct driver automatically

Cache it for future use

If Chrome is missing, download it here: Google Chrome

⚙️ Configuration (CRITICAL)
Each scraper script contains a configuration block at the top:

python
Copy code
OUTPUT_DIR = r"C:\Users\YourName\Desktop\video_crawler"
MAX_VIDEOS = 25
SCROLL_ROUNDS = 8
DOWNLOAD_VIDEOS = True
MAX_VIEW_COUNT = 20000
Variable	Purpose
OUTPUT_DIR	Root directory for all outputs
MAX_VIDEOS	Maximum Shorts collected per run
SCROLL_ROUNDS	Search depth (higher = more Shorts)
DOWNLOAD_VIDEOS	Set False for metadata-only mode
MAX_VIEW_COUNT	Filters out viral / legitimate content

▶️ How To Run
Crypto Scam Scraper

bash
Copy code
python crypto_scam_scraper.py
Giveaway Scam Scraper

bash
Copy code
python giveaway_scam_scraper.py
Gift Card Scam Scraper

bash
Copy code
python giftcard_scam_scraper.py
Chrome will open automatically and begin crawling YouTube Shorts.

📦 Output Directory Structure
text
Copy code
video_crawler/
│
├── metadata/
│   ├── youtube_shorts_crypto/
│   ├── youtube_shorts_giveaway/
│   └── youtube_shorts_giftcard/
│
├── videos/
│   ├── youtube_shorts_crypto/
│   ├── youtube_shorts_giveaway/
│   └── youtube_shorts_giftcard/
🧾 Metadata JSON Schema
Each discovered video produces a structured JSON file:

json
Copy code
{
  "video_id": "youtube_xxxxx",
  "platform": "youtube",
  "video_url": "https://www.youtube.com/shorts/...",
  "title": "...",
  "description": "...",
  "uploader": "...",
  "channel": "...",
  "upload_date": "YYYYMMDD",
  "duration": 42,
  "view_count": 15321,
  "like_count": 120,
  "comment_count": 18,
  "tags": [],
  "hashtags": ["#crypto", "#giveaway"],
  "is_short": true,
  "label": "Scam",
  "scam_type": "Crypto Scam",
  "scraped_at": "2026-01-07 10:12:00",
  "scraper_id": "HOSTNAME"
}
🎯 Use Cases
Machine learning dataset generation

Scam trend analysis

Platform moderation tooling

Academic and security research

🛑 Common Issues & Fixes
Chrome Opens Then Closes

Install Google Chrome

Update Chrome to the latest version

CAPTCHA / No Results

Increase delays (time.sleep)

Reduce SCROLL_ROUNDS

Avoid aggressive crawling behavior

yt-dlp Errors

bash
Copy code
pip install -U yt-dlp
🚀 Scaling Recommendations
Start in metadata-only mode

Increase MAX_VIDEOS gradually

Avoid parallel scraper executions

Rotate IPs / proxies for large-scale crawls

Expect CAPTCHAs at scale

🧪 Research Notes
Keyword-based heuristics are intentionally conservative

False positives are expected

Designed for dataset generation, not enforcement

Ideal as a preprocessing step before ML classification

🛣 Roadmap
Unified scraper with category flags

Proxy & IP rotation

CSV export support

Multi-threaded metadata collection

TikTok / Instagram Reels support

ML-based scam classifier

🤝 Contributing
Contributions are welcome for:

New scam categories

Keyword heuristic improvements

Performance optimization

Dataset quality enhancements

📜 License
MIT License

Use responsibly.
