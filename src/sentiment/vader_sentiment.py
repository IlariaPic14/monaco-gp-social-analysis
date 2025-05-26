# vader_sentiment.py

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

# Inizializza VADER
vader = SentimentIntensityAnalyzer()

def compute_vader_sentiment(df, text_column="comment_raw_text"):
    """
    Aggiunge al dataframe i punteggi VADER: pos, neu, neg, compound + etichetta.
    """
    def analyze(text):
        if not isinstance(text, str) or text.strip() == "":
            return {"neg": 0, "neu": 0, "pos": 0, "compound": 0}
        return vader.polarity_scores(text)

    scores = df[text_column].apply(analyze)
    sentiment_df = pd.DataFrame(scores.tolist())
    df = pd.concat([df, sentiment_df], axis=1)

    def label(row):
        if row["compound"] >= 0.05:
            return "positive"
        elif row["compound"] <= -0.05:
            return "negative"
        else:
            return "neutral"

    df["sentiment_label"] = df.apply(label, axis=1)
    return df
