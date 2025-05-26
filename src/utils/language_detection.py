# language_detection.py

from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def add_language_column(df, text_column="comment_raw_text"):
    df = df.copy()
    df["language"] = df[text_column].apply(detect_language)
    return df
