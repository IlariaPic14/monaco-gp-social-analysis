# toxic_scoring.py

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import gc
from tqdm import tqdm
import os
import sys

# Check
file_path = "data/f1_social_clean.csv"  
if not os.path.isfile(file_path):
    print(f"Errore: file '{file_path}' non trovato.")
    sys.exit(1)

# Setup device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Carica il modello pre-addestrato
MODEL_NAME = "unitary/toxic-bert"
print("Caricamento tokenizer e modello...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.to(device)
model.eval()

# Carica il dataset
df = pd.read_csv(file_path)
df['toxicity_score'] = 0.0

# Funzione di scoring
def get_toxicity_score(inputs):
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    scores = torch.sigmoid(outputs.logits).cpu().numpy()
    return scores

# Loop di inferenza
print("Inizio inferenza sul dataset...")
for i in tqdm(range(0, len(df), 16), desc="Valutazione tossicità"):
    batch = df.iloc[i:i+16]
    sentences = batch['comment_raw_text'].tolist()
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, max_length=128, truncation=True)
    scores = get_toxicity_score(inputs)
    for j, row in batch.iterrows():
        toxicity_score = scores[j % batch.shape[0]][0]
        df.at[j, "toxicity_score"] = toxicity_score
    del inputs, scores
    torch.cuda.empty_cache()
    gc.collect()

# Salvataggio output
output_file = "data/sentiment_score_toxicbert.csv"
df.to_csv(output_file, index=False)
print(f"Salvato in '{output_file}'")
