import pandas as pd
from roberta_sentiment import compute_roberta_sentiment

INPUT = "data/f1_social_labeled.csv"
OUTPUT = "data/f1_social_sentiment_roberta.csv"

df = pd.read_csv(INPUT)
df_roberta = compute_roberta_sentiment(df, batch_size=64)
df_roberta.to_csv(OUTPUT, index=False, encoding="utf-8")

print(f"File RoBERTa salvato: {OUTPUT}")
