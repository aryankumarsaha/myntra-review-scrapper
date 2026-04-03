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

    result = {
        "total_reviews": len(df),
        "avg_rating": df["Rating"].mean(),
        "avg_price": df["Price"].mean()
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)