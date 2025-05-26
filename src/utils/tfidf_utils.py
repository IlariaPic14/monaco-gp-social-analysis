from sklearn.feature_extraction.text import TfidfVectorizer

def compute_tfidf(corpus, max_df=0.9, min_df=2):
    """
    Trasforma una lista di testi in una matrice TF-IDF.
    """
    vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return tfidf_matrix, vectorizer
