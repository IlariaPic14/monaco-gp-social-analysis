# preprocessing_pipeline.py

import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from src.utils.language_detection import add_language_column


nltk.download('stopwords')

SUPPORTED_LANGUAGES = {
    "en": "english",
    "it": "italian",
    "fr": "french",
    "de": "german",
    "es": "spanish",
    "pt": "portuguese",
    "nl": "dutch",
}

def remove_emojis(text):
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def preprocess_text(text, lang):
    if not isinstance(text, str):
        return ""
    text = remove_emojis(text)
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    tokens = text.split()

    if lang in SUPPORTED_LANGUAGES:
        lang_code = SUPPORTED_LANGUAGES[lang]
        stop_words = set(stopwords.words(lang_code))
        stemmer = SnowballStemmer(lang_code)
        tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

    return " ".join(tokens)

def add_clean_text_column(df, text_column="comment_raw_text", lang_column="language"):
    df = df.copy()
    df["text_clean"] = df.apply(lambda row: preprocess_text(row[text_column], row[lang_column]), axis=1)
    return df

# === Main execution ===
if __name__ == "__main__":
    INPUT = "data/f1_social_dataset.csv"
    OUTPUT = "data/f1_social_clean.csv"

    df = pd.read_csv(INPUT)
    df = add_language_column(df)              
    df = add_clean_text_column(df)           
    df.to_csv(OUTPUT, index=False, encoding="utf-8")

    print(f"File salvato con lingua + testo pulito: {OUTPUT}")

