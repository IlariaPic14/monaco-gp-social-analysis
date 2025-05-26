# roberta_sentiment.py

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from tqdm import tqdm

# Carica tokenizer e modello
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()  # Disattiva dropout
LABELS = ["negative", "neutral", "positive"]

def compute_roberta_sentiment(df, text_column="comment_raw_text", batch_size=64):
    texts = df[text_column].fillna("").astype(str).tolist()
    sentiments = []

    for i in tqdm(range(0, len(texts), batch_size), desc="RoBERTa batching"):
        batch_texts = texts[i:i+batch_size]
        encoded_input = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
        
        with torch.no_grad():
            output = model(**encoded_input)
        
        scores = softmax(output.logits.numpy(), axis=1)
        batch_labels = scores.argmax(axis=1)

        for idx in range(len(batch_texts)):
            sentiments.append({
                "roberta_sentiment": LABELS[batch_labels[idx]],
                "roberta_neg": scores[idx][0],
                "roberta_neu": scores[idx][1],
                "roberta_pos": scores[idx][2]
            })

    sentiment_df = pd.DataFrame(sentiments)
    return pd.concat([df.reset_index(drop=True), sentiment_df], axis=1)
