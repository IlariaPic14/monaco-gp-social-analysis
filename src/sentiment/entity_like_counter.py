import pandas as pd
import spacy
from collections import defaultdict
import json

# Carica il modello spaCy
nlp = spacy.load("en_core_web_sm")

# === CONFIG ===
INPUT_CSV = "data/f1_social_sentiment_roberta.csv"  
OUTPUT_JSON = "reports/cluster_entity_likes.json"

# === Carica il dataset ===
df = pd.read_csv(INPUT_CSV)

# === Funzione per estrarre entità e sommare i like ===
def extract_entity_likes(df):
    cluster_entity_likes = defaultdict(lambda: defaultdict(int))

    for _, row in df.iterrows():
        cluster = str(row["theme_cluster"])
        text = str(row["text_clean"])
        likes = int(row["like_count"]) if not pd.isna(row["like_count"]) else 0

        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"PERSON", "ORG"}:
                entity_name = ent.text.strip().lower()
                cluster_entity_likes[cluster][entity_name] += likes

    return {k: dict(v) for k, v in cluster_entity_likes.items()}

# === Esecuzione ===
entity_likes = extract_entity_likes(df)

# === Salva il risultato in un file JSON ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(entity_likes, f, indent=2, ensure_ascii=False)

print(f"File salvato: {OUTPUT_JSON}")
