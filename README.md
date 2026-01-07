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
