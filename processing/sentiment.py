_sentiment_pipeline = None

def _get_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        from transformers import pipeline
        # Load model once and cache it in memory
        _sentiment_pipeline = pipeline("sentiment-analysis")
    return _sentiment_pipeline

def analyze_sentiment(df):
    if df is None or df.empty:
        return df

    sentiment_pipeline = _get_pipeline()
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