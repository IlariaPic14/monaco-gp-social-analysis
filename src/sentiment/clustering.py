
import pandas as pd
import json
from src.utils.tfidf_utils import compute_tfidf
from src.utils.clustering_utils import cluster_texts
from src.utils.keyword_utils import extract_top_keywords_per_cluster, generate_cluster_labels_from_keywords

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


if __name__ == "__main__":
    INPUT_PATH = "data/f1_social_clean.csv"
    OUTPUT_CSV = "data/f1_social_labeled.csv"
    OUTPUT_LABELS = "data/cluster_descriptions.json"

    # 1. Carica il dataset
    df = pd.read_csv(INPUT_PATH)

    # 2. Filtra testi in inglese
    df = df[(df["language"] == "en") & (df["text_clean"].notna())]

    # 3. TF-IDF
    tfidf_matrix, vectorizer = compute_tfidf(df["text_clean"])

    # 4. Clustering
    kmeans_model, labels = cluster_texts(tfidf_matrix, k=6)
    df["theme_cluster"] = labels

    # 5. Parole chiave
    top_keywords = extract_top_keywords_per_cluster(tfidf_matrix, labels, vectorizer)

    # 6. Etichette testuali
    cluster_labels = generate_cluster_labels_from_keywords(top_keywords)

    # 7. Salvataggio
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    with open(OUTPUT_LABELS, "w", encoding="utf-8") as f:
        json.dump(cluster_labels, f, ensure_ascii=False, indent=2)

    print(f"File CSV salvato: {OUTPUT_CSV}")
    print(f"Etichette tematiche salvate in: {OUTPUT_LABELS}")
