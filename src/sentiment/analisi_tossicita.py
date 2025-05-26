# analisi_tossicita.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    print("=== Analisi Tossicità per Social Media ===\n")

    # Percorso del file CSV
    csv_path = "data/sentiment_score_toxicbert.csv"

    if not os.path.exists(csv_path):
        print(f"Errore: File non trovato in '{csv_path}'")
        return

    # Caricamento del dataset
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except Exception as e:
        print(f"Errore nella lettura del file: {e}")
        return

    print("\nAnteprima del dataset:")
    print(df.head())

    # Nomi delle colonne
    colonna_social = 'social_media'
    colonna_tossicita = 'toxicity_score'

    # Controllo colonne
    if colonna_social not in df.columns or colonna_tossicita not in df.columns:
        print("Errore: Controlla i nomi delle colonne nel dataset!")
        return

    # Calcolo tossicità media per social
    tossicita_media = df.groupby(colonna_social)[colonna_tossicita].mean().sort_values(ascending=False)

    # Stampa risultati
    print("\nTossicità media per social media:")
    print(tossicita_media)

    print(f"\nIl social più tossico è: {tossicita_media.idxmax()} con un punteggio medio di {tossicita_media.max():.2f}")

    # Crea cartella 'reports' se non esiste
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Salva il grafico in reports
    plt.figure(figsize=(10, 6))
    tossicita_media.plot(kind='bar', color='tomato', title='Tossicità Media per Social Media')
    plt.ylabel('Tossicità Media')
    plt.xlabel('Social Media')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_path = os.path.join(reports_dir, "tossicita_media_social.png")
    plt.savefig(output_path)
    plt.close()

    print(f"\nGrafico salvato in: {output_path}")

if __name__ == "__main__":
    main()
