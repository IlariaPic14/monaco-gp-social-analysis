from src.sentiment.time_series_sentiment import (
    generate_theme_daily_sentiment,
    plot_sentiment_trend,
    plot_sentiment_trend_by_cluster,
)

if __name__ == "__main__":
    input_path = "data/f1_social_sentiment_roberta.csv"
    output_json = "reports/theme_daily_sentiment.json"

    sentiment_df = generate_theme_daily_sentiment(input_path, output_json)
    plot_sentiment_trend(sentiment_df)
    plot_sentiment_trend_by_cluster(sentiment_df)
