from transformers import pipeline

# Load model once
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(df):
    if df is None or df.empty:
        return df

    sentiments = []
    scores = []

    for comment in df["Comment"]:
        try:
            result = sentiment_pipeline(str(comment)[:512])[0]
            sentiments.append(result["label"])
            scores.append(result["score"])
        except:
            sentiments.append("NEUTRAL")
            scores.append(0)

    df["Sentiment"] = sentiments
    df["Confidence"] = scores

    return df