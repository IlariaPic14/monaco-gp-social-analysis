import praw
import json
from datetime import datetime
from pathlib import Path
import praw
from src.utils.config import (

    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    REDDIT_REFRESH_TOKEN,
)

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    refresh_token=REDDIT_REFRESH_TOKEN,
    user_agent=REDDIT_USER_AGENT
)


def fetch_reddit_data(query, subreddit_name="formula1", limit=5):
    print(f"🔎 Cercando '{query}' in r/{subreddit_name}...")
    subreddit = reddit.subreddit(subreddit_name)
    results = []

    try:
        for submission in subreddit.search(query, limit=limit):
            submission.comments.replace_more(limit=0)
            for i, comment in enumerate(submission.comments.list()):
                text = comment.body.strip()
                if not text:
                    continue

                record = {
                    "content_id": comment.id,
                    "observation_time": datetime.utcnow().isoformat() + "Z",
                    "user": comment.author.name if comment.author else "anonymous",
                    "user_location": "",
                    "social_media": "Reddit",
                    "publish_date": datetime.utcfromtimestamp(comment.created_utc).isoformat() + "Z",
                    "geo_location": None,
                    "comment_raw_text": text,
                    "emoji": [c for c in text if c in '😬🏎️🥇🚀🔥'],
                    "reference_post_url": f"https://www.reddit.com{comment.permalink}",
                    "like_count": comment.score,
                    "reply_count": 0,
                    "repost_count": 0,
                    "quote_count": 0,
                    "bookmark_count": 0,
                    "content_type": "comment"
                }

                results.append(record)

    except Exception as e:
        print(f" Errore: {e}")

    return results

if __name__ == "__main__":
    query = "Monaco GP 2025"
    output_path = Path("data/reddit_monaco_gp.json")

    data = fetch_reddit_data(query=query, subreddit_name="formula1", limit=100)

    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing_ids = {item["content_id"] for item in existing}
    new_data = [item for item in data if item["content_id"] not in existing_ids]
    combined = existing + new_data

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f" Salvati {len(new_data)} nuovi commenti (totale: {len(combined)}) in reddit_monaco_gp.json")

