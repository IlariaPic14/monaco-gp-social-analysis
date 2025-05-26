# youtube_search.py

from youtubesearchpython import VideosSearch

def get_video_ids(query, max_results=50):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()
    video_ids = []

    for video in results["result"]:
        video_ids.append({
            "id": video["id"],
            "title": video["title"],
            "link": video["link"]
        })

    return video_ids
