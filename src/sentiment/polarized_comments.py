import pandas as pd

def extract_polarized_comments(df, neg_threshold=0.9, pos_threshold=0.9, top_n=10):
    # Commenti più negativi
    top_negative = df[df["neg"] >= neg_threshold].sort_values(by="neg", ascending=False).head(top_n)
    
    # Commenti più positivi
    top_positive = df[df["pos"] >= pos_threshold].sort_values(by="pos", ascending=False).head(top_n)
    
    return top_negative, top_positive
