import os
import json
import time
import socket
import random
from collections import deque
from urllib.parse import quote_plus
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ==================================================
# CONFIG
# ==================================================
OUTPUT_DIR = r"C:\Users\Jules Gregory\Desktop\video_crawler"  # full path
MAX_VIDEOS = 25 # change to 2000 later
SCROLL_ROUNDS = 8  # increase for better Shorts discovery
DOWNLOAD_VIDEOS = True  # set True if you want videos
MAX_VIEW_COUNT = 20000  # ignore videos with more than (ex: 20k views)

# YouTube Shorts giveaway scam queries
SEARCH_QUERIES = [
    "free iphone giveaway", "free ps5 giveaway", "free macbook giveaway",
    "free ipad giveaway", "free airpods giveaway", "free gaming pc giveaway",
    "free nintendo switch giveaway", "free laptop giveaway", "free phone giveaway",
    "cash giveaway", "paypal giveaway", "venmo giveaway", "cashapp giveaway",
    "free money giveaway", "bitcoin giveaway", "crypto giveaway",
    "giveaway link in bio", "giveaway click link", "enter giveaway",
    "win free iphone", "guaranteed winner giveaway", "everyone wins giveaway",
    "fake giveaway", "giveaway scam shorts", "prize giveaway",
    "share and win", "tag friends giveaway", "comment to win",
    "celebrity giveaway", "influencer giveaway", "mrbeast giveaway scam"
]

# Giveaway scam indicator keywords
GIVEAWAY_SCAM_KEYWORDS = [
    "giveaway", "free giveaway", "win free", "enter to win", "prize draw",
    "free iphone", "free ps5", "free macbook", "free ipad", "free airpods",
    "free gaming pc", "free nintendo switch", "free xbox", "free phone", "free laptop",
    "cash giveaway", "paypal money", "venmo cash", "cashapp money", "free money",
    "bitcoin giveaway", "crypto giveaway", "eth giveaway", "btc giveaway",
    "click link", "link in bio", "link below", "check bio", "visit link",
    "go to website", "check description", "dm for details", "message to claim",
    "swipe up", "tap link", "click here to enter",
    "limited time", "hurry", "ends soon", "only today", "24 hours", "ending now",
    "guaranteed winner", "everyone wins", "you won", "congratulations you won",
    "claim prize", "claim now", "redeem prize", "verify to claim", "collect prize",
    "tag friends", "share post", "comment below", "follow and win", "like and win",
    "must follow", "turn on notifications", "subscribe to enter",
    "screenshot proof", "legit giveaway", "not fake", "real giveaway",
    "100% real", "no scam", "trusted", "verified giveaway",
    "working 2024", "working 2025", "still active", "winners announced",
    "free stuff", "free tech", "free devices", "free electronics"
]

# ==================================================
# UTILS
# ==================================================
def is_giveaway_scam(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(k in t for k in GIVEAWAY_SCAM_KEYWORDS)

def extract_hashtags(description: str, tags: list) -> list:
    hashtags = []
    if description:
        hashtags.extend([w for w in description.split() if w.startswith('#')])
    if tags:
        hashtags.extend([f"#{tag}" for tag in tags if tag])
    return list(set(hashtags)) if hashtags else None

def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")  # uncomment to run without opening Chrome
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ==================================================
# DISCOVERY
# ==================================================
def youtube_shorts_search_url(query):
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}&sp=EgIYAQ%3D%3D"

def discover_video_links(driver, url):
    driver.get(url)
    time.sleep(5)
    for i in range(SCROLL_ROUNDS):
        driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight);")
        time.sleep(random.uniform(2, 3))
        print(f"  Scroll {i+1}/{SCROLL_ROUNDS}")
    links = driver.execute_script("""
        return Array.from(document.querySelectorAll('a#video-title, a.ytd-thumbnail'))
            .map(a => a.href)
            .filter(h => h && (h.includes('shorts/') || h.includes('watch?v=')));
    """)
    unique_links = list(set(links))
    print(f"  Found {len(unique_links)} unique videos")
    return unique_links

# ==================================================
# METADATA EXTRACTION
# ==================================================
def extract_metadata(url):
    try:
        ydl_opts = {"quiet": True, "skip_download": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Check duration
        duration = info.get("duration", 0)
        if duration > 60:
            return None
        
        # Check view count
        view_count = info.get("view_count", 0)
        if view_count and view_count > MAX_VIEW_COUNT:
            print(f"  ⊗ Too many views ({view_count:,} > {MAX_VIEW_COUNT:,}) - skipped")
            return None
        
        title = info.get('title', '')
        description = info.get('description', '')
        tags = info.get('tags', [])
        text_blob = f"{title} {description} {' '.join(tags)}"
        if not is_giveaway_scam(text_blob):
            return None
        hashtags = extract_hashtags(description, tags)
        video_id = info['id']
        shorts_url = f"https://www.youtube.com/shorts/{video_id}"
        return {
            "video_id": f"youtube_{video_id}",
            "platform": "youtube",
            "video_url": shorts_url,
            "title": title,
            "description": description,
            "uploader": info.get("uploader"),
            "channel": info.get("channel"),
            "upload_date": info.get("upload_date"),
            "duration": duration,
            "view_count": view_count,
            "like_count": info.get("like_count"),
            "comment_count": info.get("comment_count"),
            "tags": tags if tags else [],
            "hashtags": hashtags,
            "is_short": True,
            "label": "Scam",
            "scam_type": "Giveaway Scam",
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scraper_id": socket.gethostname()
        }
    except Exception as e:
        print(f"  Error extracting metadata: {e}")
        return None

# ==================================================
# SAVE
# ==================================================
def save_metadata(meta):
    base = os.path.join(OUTPUT_DIR, "metadata", "youtube_shorts_giveaway")
    os.makedirs(base, exist_ok=True)
    path = os.path.join(base, f"{meta['video_id']}.json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved: {meta['video_id']} ({meta['view_count']:,} views)")

def download_video(url, video_id):
    base = os.path.join(OUTPUT_DIR, "videos", "youtube_shorts_giveaway")
    os.makedirs(base, exist_ok=True)
    path = os.path.join(base, f"{video_id}.mp4")
    if os.path.exists(path):
        print(f"  ⊗ Already downloaded: {video_id}")
        return
    ydl_opts = {"outtmpl": path, "format": "bestvideo+bestaudio/best", "merge_output_format": "mp4", "quiet": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"  ⬇ Downloaded: {video_id}")
    except Exception as e:
        print(f"  Error downloading: {e}")

# ==================================================
# MAIN CRAWLER
# ==================================================
def main():
    print("=" * 70)
    print("YouTube Shorts Giveaway Scam Scraper")
    print(f"Max views: {MAX_VIEW_COUNT:,}")
    print("=" * 70)
    driver = setup_driver()
    visited = set()
    collected = 0
    queue = deque([youtube_shorts_search_url(q) for q in SEARCH_QUERIES])
    try:
        while queue and collected < MAX_VIDEOS:
            page = queue.popleft()
            print(f"\n[>] Crawling: {page}")
            try:
                links = discover_video_links(driver, page)
            except Exception as e:
                print(f"  Error discovering links: {e}")
                continue
            for video_url in links:
                if video_url in visited or collected >= MAX_VIDEOS:
                    continue
                visited.add(video_url)
                print(f"\n[{collected+1}/{MAX_VIDEOS}] Processing: {video_url}")
                meta = extract_metadata(video_url)
                if not meta:
                    print("  ⊗ Filtered out (not a scam, wrong duration, or too many views)")
                    continue
                save_metadata(meta)
                if DOWNLOAD_VIDEOS:
                    download_video(video_url, meta["video_id"])
                collected += 1
                print(f"  ✓ Total collected: {collected}/{MAX_VIDEOS}")
                if meta.get("channel") and collected < MAX_VIDEOS:
                    channel_name = meta['channel'].replace(' ', '')
                    channel_shorts_url = f"https://www.youtube.com/@{channel_name}/shorts"
                    if channel_shorts_url not in visited:
                        queue.append(channel_shorts_url)
                        print(f"  + Added channel Shorts to queue")
                time.sleep(random.uniform(2, 5))
        print("\n" + "=" * 70)
        print(f"✓ Scraping complete! Collected {collected} giveaway scam Shorts")
        print("=" * 70)
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
    finally:
        driver.quit()
        print(f"\nFinal count: {collected} videos")
        print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()