from sklearn.cluster import KMeans
import numpy as np

def cluster_texts(tfidf_matrix, k=6):
    """
    Applica KMeans alla matrice TF-IDF.
    """
    model = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = model.fit_predict(tfidf_matrix)
    return model, labels

