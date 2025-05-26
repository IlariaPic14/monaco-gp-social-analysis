# keyword_utils.py

import numpy as np
from collections import defaultdict

def extract_top_keywords_per_cluster(tfidf_matrix, labels, vectorizer, top_n=10):
    feature_names = vectorizer.get_feature_names_out()
    top_keywords = defaultdict(list)

    for cluster_id in sorted(set(labels)):
        cluster_indices = np.where(labels == cluster_id)[0]
        cluster_matrix = tfidf_matrix[cluster_indices]
        mean_tfidf = cluster_matrix.mean(axis=0).A1
        sorted_indices = mean_tfidf.argsort()[::-1][:top_n]
        top_keywords[cluster_id] = [feature_names[i] for i in sorted_indices]

    return dict(top_keywords)

def generate_cluster_labels_from_keywords(top_keywords_dict):
    cluster_labels = {}
    for cluster_id, keywords in top_keywords_dict.items():
        keywords_str = ", ".join(keywords)
        label = f"Cluster {cluster_id}: tema principale basato su {keywords_str}"
        cluster_labels[str(cluster_id)] = label
    return cluster_labels
