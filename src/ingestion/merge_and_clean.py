import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# === CONFIG ===
input_jsons = [
    "data/gui_extracted_comments.json",
    "data/instagram_multi_profiles.json",
    "data/youtube_monaco_gp.json",
    "data/reddit_monaco_gp.json"
]
tiktok_csv = "data/tiktok_ingestion.csv"
output_csv = "data/f1_social_dataset.csv"

# === SCHEMA UFFICIALE ===
schema = {
    "content_id": "",
    "observation_time": "",
    "user": "",
    "user_location": "",
    "social_media": "",
    "publish_date": "",
    "geo_location": None,
    "comment_raw_text": "",
    "emoji": [],
    "reference_post_url": "",
    "like_count": 0,
    "reply_count": 0,
    "repost_count": 0,
    "quote_count": 0,
    "bookmark_count": 0,
    "content_type": ""
}

# === Mappa nomi città → coordinate geografiche ===
LOCATION_MAP = {
    "Monaco": (43.7384, 7.4246),
    "Monte Carlo": (43.7396, 7.4276),
    "Monaco Grand Prix": (43.7384, 7.4246)
}

def convert_geo_location(val):
    if pd.isna(val):
        return None
    val = str(val).strip()
    return LOCATION_MAP.get(val, None)

def normalize_dataframe(df):
    for col, default in schema.items():
        if col not in df.columns:
            df[col] = default
        else:
            if col == "geo_location":
                def process_geo(val):
                    if pd.isna(val) or val in ["", "None", "nan"]:
                        return 0
                    if isinstance(val, (list, tuple)) and len(val) == 2:
                        return tuple(val)
                    try:
                        val_json = json.loads(val) if isinstance(val, str) and val.startswith("[") else val
                        if isinstance(val_json, (list, tuple)) and len(val_json) == 2:
                            return tuple(val_json)
                    except:
                        pass
                    val_str = str(val).strip()
                    return LOCATION_MAP.get(val_str, 0)
                
                df[col] = df[col].apply(process_geo)

            elif isinstance(default, list):
                df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])
            elif isinstance(default, (int, float)):
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(default).astype(int)
            elif isinstance(default, str):
                df[col] = df[col].apply(lambda x: str(x) if pd.notnull(x) else default)
            else:
                df[col] = df[col].apply(lambda x: x if pd.notnull(x) else default)

    df["content_type"] = df["content_type"].apply(lambda x: "post" if str(x).lower() == "post" else "commento")
    return df[list(schema.keys())]

def load_json_files(files):
    all_data = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    return pd.DataFrame(all_data)

def load_and_process_tiktok(csv_path):
    df = pd.read_csv(csv_path)

    df = df.rename(columns={
        "Content_ID": "content_id",
        "Observation_time": "observation_time",
        "User": "user",
        "User_Location": "user_location",
        "social_media": "social_media",
        "publish _date": "publish_date",
        "Geo_location": "geo_location",
        "comment_raw_text": "comment_raw_text",
        "emoji": "emoji",
        "reference": "reference_post_url",
        "like_count": "like_count",
        "reply_count": "reply_count",
        "Repost_Count": "repost_count",
        "QUOTE_Count": "quote_count",
        "BOOKMARK_COUNT": "bookmark_count",
        "CONTENT TYPE": "content_type"
    })

    df["geo_location"] = df["geo_location"].apply(convert_geo_location)
    df["emoji"] = df["emoji"].fillna("").apply(lambda x: list(str(x)))
    df["comment_raw_text"] = df["comment_raw_text"].fillna("")
    df["content_type"] = df["content_type"].apply(lambda x: "post" if str(x).lower() == "post" else "commento")
    df["reference_post_url"] = df["reference_post_url"].fillna("")

    for col in ["observation_time", "publish_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    return df

# === MERGE & NORMALIZZA ===
df_json = load_json_files(input_jsons)
df_tiktok = load_and_process_tiktok(tiktok_csv)

df_combined = pd.concat([df_json, df_tiktok], ignore_index=True)
df_clean = normalize_dataframe(df_combined)

# FIX formato data e FILTRO: solo contenuti del 2025
def parse_iso_date(x):
    try:
        return pd.to_datetime(x, utc=True)
    except:
        return pd.NaT

df_clean["publish_date"] = df_clean["publish_date"].apply(parse_iso_date)

print(f"Righe totali PRIMA del filtro 2025: {len(df_clean)}")
print(f"Conteggio per piattaforma PRIMA del filtro:\n{df_clean['social_media'].value_counts()}")

df_clean = df_clean[df_clean["publish_date"].dt.year == 2025]

print(f"Righe totali DOPO il filtro 2025: {len(df_clean)}")
print(f"Conteggio per piattaforma DOPO il filtro:\n{df_clean['social_media'].value_counts()}")

# === ESPORTA ===
df_clean.to_csv(output_csv, index=False, encoding="utf-8")
print(f"Dataset finale pulito salvato in: {output_csv} con {len(df_clean)} righe.")
