import pandas as pd
import json
import os
import matplotlib.pyplot as plt

def generate_theme_daily_sentiment(input_csv, output_json):
    """
    Calcola l'andamento giornaliero del sentiment positivo (RoBERTa)
    per ciascun cluster tematico.
    Salva i risultati in formato JSON.
    """
    df = pd.read_csv(input_csv)

    # Parsing e pulizia date
    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")
    df = df.dropna(subset=["publish_date"])
    df["date"] = df["publish_date"].dt.date

    # Media giornaliera del sentiment positivo per cluster
    sentiment_trend = (
        df.groupby(["theme_cluster", "date"])["roberta_pos"]
        .mean()
        .reset_index()
        .rename(columns={"roberta_pos": "avg_roberta_pos"})
    )

    # Salvataggio JSON
    sentiment_trend["date"] = sentiment_trend["date"].astype(str)
    sentiment_trend.to_json(output_json, orient="records", indent=2, force_ascii=False)

    print(f"JSON salvato: {output_json}")
    return sentiment_trend


def plot_sentiment_trend(sentiment_df):
    """
    Grafico unico con tutte le linee di sentiment per cluster tematico.
    """
    plt.figure(figsize=(12, 6))
    for cluster_id in sorted(sentiment_df["theme_cluster"].unique()):
        cluster_data = sentiment_df[sentiment_df["theme_cluster"] == cluster_id]
        plt.plot(cluster_data["date"], cluster_data["avg_roberta_pos"], marker="o", label=f"Cluster {cluster_id}")

    plt.title("Andamento giornaliero del sentiment (RoBERTa) per cluster tematico")
    plt.xlabel("Data")
    plt.ylabel("Sentiment positivo medio")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_sentiment_trend_by_cluster(sentiment_df, output_folder="reports/plots"):
    """
    Crea un grafico separato per ogni cluster tematico e lo salva in PNG.
    """
    os.makedirs(output_folder, exist_ok=True)

    cluster_ids = sorted(sentiment_df["theme_cluster"].unique())
    for cluster_id in cluster_ids:
        cluster_data = sentiment_df[sentiment_df["theme_cluster"] == cluster_id]

        plt.figure(figsize=(10, 5))
        plt.plot(cluster_data["date"], cluster_data["avg_roberta_pos"], marker="o", color="tab:blue")
        plt.title(f"Sentiment giornaliero - Cluster {cluster_id}")
        plt.xlabel("Data")
        plt.ylabel("Sentiment positivo medio (RoBERTa)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        filename = f"{output_folder}/cluster_{cluster_id}_sentiment.png"
        plt.savefig(filename)
        print(f"Grafico salvato: {filename}")
        plt.close()
