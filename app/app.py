from flask import Flask, jsonify
from database.db import load_data

app = Flask(__name__)

@app.route("/")
def home():
    return "Myntra Data API Running 🚀"

@app.route("/reviews")
def get_reviews():
    df = load_data()
    return df.to_json(orient="records")

@app.route("/summary")
def summary():
    df = load_data()

    positive_count = len(df[df["Sentiment"] == "POSITIVE"])
    negative_count = len(df[df["Sentiment"] == "NEGATIVE"])
    total = len(df)

    positive_ratio = positive_count / total if total > 0 else 0

    decision = "Buy" if positive_ratio >= 0.6 else "Not Buy"

    result = {
        "total_reviews": total,
        "avg_rating": df["Rating"].mean(),
        "avg_price": df["Price"].mean(),
        "positive_reviews": positive_count,
        "negative_reviews": negative_count,
        "positive_ratio": positive_ratio,
        "decision": decision
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)