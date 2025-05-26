# src/ingestion/instagram_profiles_scraper.py

import instaloader
from instaloader import Profile
from datetime import datetime
import json
import os



COOKIES_PATH = os.path.join(os.path.dirname(__file__), "..", "utils", "instagram_cookies_scraper.json")
COOKIES_PATH = os.path.abspath(COOKIES_PATH)


def load_cookies():
    with open(COOKIES_PATH, "r", encoding="utf-8") as f:
        cookies_list = json.load(f)
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
    return cookies_dict



def load_context_from_cookie():
    L = instaloader.Instaloader(
        download_pictures=False,
        download_comments=False,
        download_videos=False
    )
    cookies = load_cookies()
    L.context._session.cookies.update(cookies)
    L.context._session.headers.update({"X-CSRFToken": cookies["csrftoken"]})
    return L



def extract_posts_from_profile(profile_name, max_posts=10):
    L = load_context_from_cookie()
    profile = Profile.from_username(L.context, profile_name)
    posts = profile.get_posts()

    data = []
    for i, post in enumerate(posts):
        if i >= max_posts:
            break

        text = post.caption or ""

        post_data = {
            "content_id": str(post.mediaid),
            "observation_time": datetime.utcnow().isoformat() + "Z",
            "user": post.owner_username,
            "user_location": "",
            "social_media": "Instagram",
            "publish_date": post.date_utc.isoformat() + "Z",
            "geo_location": (post.location.lat, post.location.lng) if post.location else None,
            "comment_raw_text": text,
            "emoji": [c for c in text if c in '😬\ud83c\udfce\ufe0f\ud83e\udd47\ud83d\ude80\ud83d\udd25'],
            "reference_post_url": f"https://www.instagram.com/p/{post.shortcode}/",
            "like_count": post.likes,
            "reply_count": post.comments,
            "repost_count": 0,
            "quote_count": 0,
            "bookmark_count": 0,
            "content_type": "post"
        }

        data.append(post_data)

    return data


if __name__ == "__main__":
    profile_names = [
        "f1",
        "redbullracing",
        "scuderiaferrari",
        "mercedesamgf1",
        "mclaren",
        "alphataurif1",
        "astonmartinf1",
        "alpinef1team"
    ]

    # === 1. Carica i post già esistenti (se presenti)
    existing_posts = []
    existing_ids = set()
    output_path = "data/instagram_multi_profiles.json"

    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing_posts = json.load(f)
            existing_ids = {p["content_id"] for p in existing_posts}

    # === 2. Estrai nuovi post
    new_posts = []
    for profile in profile_names:
        print(f"\U0001F50D Estrazione da @{profile}...")
        try:
            posts = extract_posts_from_profile(profile, max_posts=5)
            for post in posts:
                if post["content_id"] not in existing_ids:
                    new_posts.append(post)
                    existing_ids.add(post["content_id"])
        except Exception as e:
            print(f" Errore con @{profile}: {e}")

    # === 3. Unisci ed esporta
    all_posts = existing_posts + new_posts

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"\n Aggiunti {len(new_posts)} nuovi post. Totale ora: {len(all_posts)} post salvati in {output_path}")

