# youtube_ingestion.py

from youtube_comment_downloader import YoutubeCommentDownloader
from src.utils.youtube_search import get_video_ids
from datetime import datetime
import json
from pathlib import Path

def scrape_youtube_comments(video_id, max_comments=100):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(
        f"https://www.youtube.com/watch?v={video_id}",
        sort_by=0
    )

    data = []
    for i, comment in enumerate(comments):
        if i >= max_comments:
            break

        text = comment.get('text', '').strip()
        if not text:
            continue

        record = {
            "content_id": f"youtube_{video_id}_{i}",
            "observation_time": datetime.utcnow().isoformat() + "Z",
            "user": comment.get('author', 'anonymous'),
            "user_location": "",
            "social_media": "YouTube",
            "publish_date": datetime.utcnow().isoformat() + "Z",
            "geo_location": None,
            "comment_raw_text": text,
            "emoji": [c for c in text if c in '😬🏎️🥇🚀🔥'],
            "reference_post_url": f"https://www.youtube.com/watch?v={video_id}",
            "like_count": int(comment.get('votes', '0').replace('.', '').replace(',', '').strip()),

            "reply_count": 0,
            "repost_count": 0,
            "quote_count": 0,
            "bookmark_count": 0,
            "content_type": "comment"
        }

        data.append(record)

    return data

# --- ESECUZIONE COMPLETA ---
if __name__ == "__main__":
    query = "Monaco GP 2025"
    video_list = get_video_ids(query, max_results=50)

    all_data = []
    for video in video_list:
        print(f"🎥 Estrazione commenti da: {video['title']}")
        comments = scrape_youtube_comments(video['id'], max_comments=100)
        all_data.extend(comments)

    # --- Salvataggio APPEND se file esiste ---
    output_path = Path("data/youtube_monaco_gp.json")

    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing_ids = {item["content_id"] for item in existing}
    new_data = [c for c in all_data if c["content_id"] not in existing_ids]

    combined = existing + new_data

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"\n Salvati {len(new_data)} nuovi commenti in append su {len(combined)} totali")

