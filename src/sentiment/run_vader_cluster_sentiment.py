import pandas as pd
from vader_sentiment import compute_vader_sentiment

INPUT = "data/f1_social_labeled.csv"
OUTPUT = "data/f1_social_sentiment_vader.csv"

df = pd.read_csv(INPUT)
df_vader = compute_vader_sentiment(df)
df_vader.to_csv(OUTPUT, index=False, encoding="utf-8")

print(f"File VADER salvato: {OUTPUT}")
