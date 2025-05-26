# -*- coding: utf-8 -*-
"""
Sentiment_Task2_Hackaton.py

Script per analisi sentiment su nomi di guidatori e analisi temporale sentiment.
Legge input da 'data/f1_social_sentiment_multilingua.csv'.
Salva i grafici nella cartella 'reports'.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict
from datetime import datetime, timezone

INPUT_FILE = os.path.join('data', 'f1_social_sentiment_multilingua_finale.csv')
REPORTS_DIR = 'report'

def assicurati_cartella(cartella):
    if not os.path.exists(cartella):
        os.makedirs(cartella)

def analisi_sentiment_nomi(file_csv):
    df = pd.read_csv(file_csv)

    colonna_testo = 'text_clean'
    colonna_sentiment = 'sentiment'

    mappa_sentiment = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }

    nomi_guidatori = ['Verstappen', 'Hamilton', 'Leclerc', 'Sainz', 'Norris', 'Russell', 'Perez', 'Alonso']

    sentiment_per_nome = defaultdict(list)

    for _, row in df.iterrows():
        testo = str(row[colonna_testo]).lower()
        sentiment_testuale = str(row[colonna_sentiment]).lower()
        sent = mappa_sentiment.get(sentiment_testuale)

        if sent is None:
            continue

        for nome in nomi_guidatori:
            if re.search(r'\b' + re.escape(nome.lower()) + r'\b', testo):
                sentiment_per_nome[nome].append(sent)

    media_sentiment = {nome: sum(valori) / len(valori) if len(valori) > 0 else 0
                       for nome, valori in sentiment_per_nome.items()}

    media_sentiment_sorted = dict(sorted(media_sentiment.items(), key=lambda x: x[1], reverse=True))

    print("\nSentiment medio per nome:")
    for nome, sent in media_sentiment_sorted.items():
        print(f"{nome}: {sent:.3f}")

    plt.figure(figsize=(10,6))
    plt.bar(media_sentiment_sorted.keys(), media_sentiment_sorted.values(), color='mediumseagreen')
    plt.title('Sentiment Medio per Nome di Guidatore')
    plt.ylabel('Sentiment Medio (-1 = negativo, 1 = positivo)')
    plt.xlabel('Nome')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    assicurati_cartella(REPORTS_DIR)
    output_path = os.path.join(REPORTS_DIR, 'sentiment_medio_per_nome.png')
    plt.savefig(output_path)
    print(f"Grafico sentiment medio per nome salvato in: {output_path}")
    plt.close()

def analisi_sentiment_temporale(file_csv):
    df = pd.read_csv(file_csv)

    df['publish_date'] = pd.to_datetime(df['publish_date'], utc=True, errors='coerce')

    mappa_sentiment = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }

    inizio_gara = datetime(2025, 5, 25, 13, 0, tzinfo=timezone.utc)
    fine_gara = datetime(2025, 5, 25, 15, 0, tzinfo=timezone.utc)

    def assegna_fase(data):
        if pd.isna(data):
            return 'Sconosciuta'
        if data < inizio_gara:
            return 'Prima'
        elif inizio_gara <= data <= fine_gara:
            return 'Durante'
        else:
            return 'Dopo'

    df['fase'] = df['publish_date'].apply(assegna_fase)

    df = df[df['sentiment'].str.lower().isin(mappa_sentiment.keys())]

    df['sentiment_val'] = df['sentiment'].str.lower().map(mappa_sentiment)

    media_sentiment_per_fase = df.groupby('fase')['sentiment_val'].mean().reindex(['Prima', 'Durante', 'Dopo'])

    plt.figure(figsize=(8,6))
    media_sentiment_per_fase.plot(kind='bar', color=['skyblue', 'orange', 'mediumseagreen'])
    plt.title("Sentiment Medio Prima, Durante e Dopo la Gara di Monaco (2025)")
    plt.ylabel("Sentiment Medio (-1 = negativo, 1 = positivo)")
    plt.xlabel("Fase Temporale")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    assicurati_cartella(REPORTS_DIR)
    output_path = os.path.join(REPORTS_DIR, 'sentiment_medio_per_fase.png')
    plt.savefig(output_path)
    print(f"Grafico sentiment medio per fase salvato in: {output_path}")
    plt.close()

def main():
    print(f"Caricamento file input da: {INPUT_FILE}")

    if not os.path.isfile(INPUT_FILE):
        print(f"Errore: file di input non trovato: {INPUT_FILE}")
        return

    analisi_sentiment_nomi(INPUT_FILE)
    analisi_sentiment_temporale(INPUT_FILE)

if __name__ == "__main__":
    main()
