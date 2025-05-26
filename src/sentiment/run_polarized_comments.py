import pandas as pd
from src.sentiment.polarized_comments import extract_polarized_comments

INPUT = "data/f1_social_sentiment_vader.csv"
OUTPUT_NEG = "reports/top_negative_comments.csv"
OUTPUT_POS = "reports/top_positive_comments.csv"

# Carica dataset
df = pd.read_csv(INPUT)

# Estrai i commenti polarizzati
top_neg, top_pos = extract_polarized_comments(df)

# Salva i risultati
top_neg.to_csv(OUTPUT_NEG, index=False, encoding="utf-8")
top_pos.to_csv(OUTPUT_POS, index=False, encoding="utf-8")

print("Top 10 commenti negativi salvati in:", OUTPUT_NEG)
print("Top 10 commenti positivi salvati in:", OUTPUT_POS)
