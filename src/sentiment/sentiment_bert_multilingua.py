
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm
import os

#  Percorsi fissi
INPUT_FILE = "data/f1_social_clean.csv"
OUTPUT_FILE = "data/f1_social_sentiment_multilingua.csv"

#  Modello pre-addestrato
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

#  Funzioni
def convert_stars_to_label(label):
    stars = int(label[0])  
    if stars <= 2:
        return "negative"
    elif stars == 3:
        return "neutral"
    else:
        return "positive"

def predict_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return "neutral"
    try:
        result = sentiment_pipeline(text[:512])  # max 512 token
        label = result[0]["label"]
        return convert_stars_to_label(label)
    except Exception as e:
        print(f"Errore su '{text[:30]}': {e}")
        return "neutral"

#  Main
def main():
    if not os.path.exists(INPUT_FILE):
        print(f" File non trovato: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    if "comment_raw_text" not in df.columns:
        print(" La colonna 'comment_raw_text' non è presente nel file.")
        return

    tqdm.pandas(desc=" Sentiment Analysis in corso...")
    df["sentiment"] = df["comment_raw_text"].progress_apply(predict_sentiment)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f" File salvato con sentiment multilingua: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
