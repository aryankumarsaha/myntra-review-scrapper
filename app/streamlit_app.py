
# .\venv\Scripts\activate
# streamlit run app/streamlit_app.py
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import load_data, save_to_db
from scraper.myntra_scraper import ScrapeReviews
from processing.clean_data import clean_data
from processing.sentiment import analyze_sentiment   # ✅ NEW

st.set_page_config(page_title="Myntra Dashboard", layout="wide")

st.title("🛍️ Myntra Product Analyzer")

if "mode" not in st.session_state:
    st.session_state.mode = None

product_input = st.text_input("🔎 Search Product", "nike shoes")
url_input = st.text_input("🔗 Paste Product URL")

col1, col2, col3 = st.columns(3)

with col1:
    search_btn = st.button("🔍 Search Products")

with col2:
    url_btn = st.button("🌐 Fetch from URL")

with col3:
    reset_btn = st.button("🔄 Reset")

if reset_btn:
    st.session_state.mode = None
    st.experimental_rerun()

# ---------------- SEARCH ----------------
if search_btn:
    with st.spinner("Scraping products..."):
        scraper = ScrapeReviews(product_input, 3)
        df = scraper.get_review_data()

        if df.empty:
            st.error("❌ No data scraped.")
            st.stop()

        df = clean_data(df)
        df = analyze_sentiment(df)   # ✅ NEW

        save_to_db(df)
        st.session_state.mode = "multi"
        st.success("✅ Products fetched!")

# ---------------- URL ----------------
if url_btn and url_input:
    with st.spinner("Fetching product..."):
        scraper = ScrapeReviews("", 1)
        df = scraper.scrape_single_product(url_input)

        if df.empty:
            st.error("❌ Could not fetch product.")
            st.stop()

        df = clean_data(df)
        df = analyze_sentiment(df)   # ✅ NEW

        save_to_db(df)
        st.session_state.mode = "single"
        st.success("✅ Product fetched!")

# ---------------- DISPLAY ----------------
if st.session_state.mode:
    df = load_data()

    if df.empty:
        st.warning("⚠️ No data available.")
        st.stop()

    # 🔥 GLOBAL AI INSIGHT
    st.subheader("🧠 AI Recommendation")

    positive_count = len(df[df["Sentiment"] == "POSITIVE"])
    negative_count = len(df[df["Sentiment"] == "NEGATIVE"])
    total = len(df)

    positive_ratio = positive_count / total if total > 0 else 0

    decision = "✅ Recommended (Buy)" if positive_ratio >= 0.6 else "❌ Not Recommended"

    st.write(f"👍 Positive: {positive_count}")
    st.write(f"👎 Negative: {negative_count}")
    st.write(f"📊 Positive Ratio: {round(positive_ratio*100, 2)}%")
    st.markdown(f"### 🛒 Decision: {decision}")

    st.markdown("---")

    # ---------------- SINGLE ----------------
    if st.session_state.mode == "single":
        st.subheader("🛍️ Product Details")

        product_name = df["Product Name"].iloc[0]
        price = df["Price"].iloc[0]
        avg_rating = round(df["Rating"].mean(), 2)

        st.write(f"### {product_name}")
        st.write(f"💰 Price: ₹{price}")
        st.write(f"⭐ Avg Rating: {avg_rating}")

        st.subheader("🟢 Positive Reviews")
        for _, row in df[df["Sentiment"] == "POSITIVE"].iterrows():
            st.write(f"✔ {row['Comment']}")

        st.subheader("🔴 Negative Reviews")
        for _, row in df[df["Sentiment"] == "NEGATIVE"].iterrows():
            st.write(f"❌ {row['Comment']}")

    # ---------------- MULTI ----------------
    elif st.session_state.mode == "multi":
        st.subheader("📦 Product-wise Insights")

        product_df = df.groupby("Product Name").agg({
            "Price": "mean",
            "Rating": "mean"
        }).reset_index()

        for _, row in product_df.iterrows():
            product = row["Product Name"]
            product_reviews = df[df["Product Name"] == product]

            st.markdown(f"### 🛍️ {product}")
            st.write(f"💰 Price: ₹{int(row['Price'])}")
            st.write(f"⭐ Avg Rating: {round(row['Rating'], 2)}")

            st.write("🟢 Positive Reviews:")
            for _, r in product_reviews[product_reviews["Sentiment"] == "POSITIVE"].iterrows():
                st.write(f"✔ {r['Comment']}")

            st.write("🔴 Negative Reviews:")
            for _, r in product_reviews[product_reviews["Sentiment"] == "NEGATIVE"].iterrows():
                st.write(f"❌ {r['Comment']}")

            st.markdown("---")