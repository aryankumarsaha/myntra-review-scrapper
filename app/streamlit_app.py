import streamlit as st
import sys
import os
import pandas as pd
import sqlite3

# Append project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import load_data, save_to_db, DB_NAME
from scraper.myntra_scraper import ScrapeReviews
from processing.clean_data import clean_data
from processing.sentiment import analyze_sentiment

# Page Config
st.set_page_config(page_title="Myntra Product Review Analyzer", layout="wide")

# Custom Modern styling (Glassmorphism & typography)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* Apply font family globally */
html, body, [data-testid="stAppViewContainer"], .stMarkdown {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6, .pdp-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

/* Custom Header with Gradient */
.header-container {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
    padding: 35px 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.4);
}

.header-title {
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}

.header-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 300;
    margin: 0;
}

/* Glassmorphic Metrics Card */
.metric-box {
    background: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.12);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 24px 16px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-bottom: 4px solid #4f46e5;
}

.metric-box:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(79, 70, 229, 0.15);
    border-bottom: 4px solid #db2777;
}

.metric-num {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 8px 0;
    background: linear-gradient(90deg, #4f46e5, #db2777);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-title {
    font-size: 0.8rem;
    color: #8E9CAE;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* Sentiment Badge Pill */
.sentiment-badge {
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.badge-positive {
    background-color: rgba(16, 185, 129, 0.12);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.badge-negative {
    background-color: rgba(239, 68, 68, 0.12);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.badge-neutral {
    background-color: rgba(107, 114, 128, 0.12);
    color: #6B7280;
    border: 1px solid rgba(107, 114, 128, 0.2);
}

/* Decision Cards */
.decision-card {
    border-radius: 16px;
    padding: 24px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.decision-buy {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.06) 0%, rgba(5, 150, 105, 0.03) 100%);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-left: 6px solid #10B981;
}

.decision-avoid {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.06) 0%, rgba(220, 38, 38, 0.03) 100%);
    border: 1px solid rgba(239, 68, 68, 0.15);
    border-left: 6px solid #EF4444;
}

/* Review Feed List Card */
.review-feed-card {
    background: rgba(128, 128, 128, 0.02);
    border: 1px solid rgba(128, 128, 128, 0.1);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
}

.review-feed-card:hover {
    border-color: rgba(79, 70, 229, 0.25);
    background: rgba(79, 70, 229, 0.01);
}

.rating-stars {
    color: #F59E0B;
    font-weight: 700;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🛍️ Myntra Product Analyzer</h1>
    <p class="header-subtitle">Dynamic reviews scraping, natural language cleaning, and AI sentiment analysis dashboard</p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "mode" not in st.session_state:
    try:
        df = load_data()
        if not df.empty:
            st.session_state.mode = "single" if len(df["Product Name"].unique()) <= 1 else "multi"
        else:
            st.session_state.mode = None
    except Exception:
        st.session_state.mode = None

# Tab Layout
tab_run, tab_dash, tab_reviews = st.tabs(["🔄 Run Pipeline / Scraper", "📊 Dashboard Insights", "💬 Review Explorer"])

# ----------------- TAB 1: RUN PIPELINE -----------------
with tab_run:
    st.subheader("⚙️ Scraping Control Center")
    st.markdown("Configure the automated scraper to gather data. The pipeline runs scraping, cleans attributes, predicts sentiment, and writes to SQLite database.")

    run_col1, run_col2 = st.columns(2)

    with run_col1:
        st.markdown("""
        <div style="background:rgba(128,128,128,0.02); padding:20px; border-radius:12px; border:1px solid rgba(128,128,128,0.08); height:100%;">
            <h4>🔍 Option A: Search Products Dynamically</h4>
            <p style="font-size:0.9rem; color:#8E9CAE;">Search Myntra by keywords, pull matching items, and analyze reviews collectively.</p>
        </div>
        """, unsafe_allow_html=True)
        product_input = st.text_input("Product Search Keyword", "nike shoes", help="e.g. adidas shoes, watch, t-shirt")
        no_of_products = st.slider("Number of Products to scrape", min_value=1, max_value=5, value=3)
        search_btn = st.button("🚀 Run Keyword Search Pipeline", use_container_width=True)

    with run_col2:
        st.markdown("""
        <div style="background:rgba(128,128,128,0.02); padding:20px; border-radius:12px; border:1px solid rgba(128,128,128,0.08); height:100%;">
            <h4>🔗 Option B: Extract Specific Product reviews</h4>
            <p style="font-size:0.9rem; color:#8E9CAE;">Analyze a single product directly using its Myntra product link.</p>
        </div>
        """, unsafe_allow_html=True)
        url_input = st.text_input("Myntra Product URL", placeholder="https://www.myntra.com/shoes/...")
        url_btn = st.button("🌐 Run Direct URL pipeline", use_container_width=True)

    st.markdown("---")

    st.subheader("⚠️ Database Utility")
    reset_col1, reset_col2 = st.columns([3, 1])
    with reset_col1:
        st.write("Need to start fresh? Resetting the database will drop the `reviews` table, clearing all stored results.")
    with reset_col2:
        reset_btn = st.button("🗑️ Reset SQLite Database", type="secondary", use_container_width=True)

    # Scrape actions
    if search_btn:
        with st.spinner("🕷️ Initializing Myntra Selenium scraper..."):
            scraper = ScrapeReviews(product_input, no_of_products)
            df_raw = scraper.get_review_data()

            if df_raw.empty:
                st.error("❌ No products/reviews were found.")
                if hasattr(scraper, 'error_log') and scraper.error_log:
                    st.warning("🔍 Scraper Diagnostic Log Trace:")
                    for log in scraper.error_log:
                        st.markdown(f"- {log}")
                st.stop()

            st.info("🧹 Performing text cleaning and conversions...")
            df_cleaned = clean_data(df_raw)

            st.info("🧠 Performing Sentiment Analysis using HuggingFace Transformers...")
            df_processed = analyze_sentiment(df_cleaned)

            save_to_db(df_processed)
            st.session_state.mode = "multi"
            st.success(f"🎉 Success! Processed & saved {len(df_processed)} reviews for search: '{product_input}'.")
            st.rerun()

    if url_btn:
        if not url_input.strip():
            st.warning("⚠️ Please provide a valid product URL.")
        else:
            with st.spinner("🕷️ Fetching single product reviews..."):
                scraper = ScrapeReviews("", 1)
                df_raw = scraper.scrape_single_product(url_input)

                if df_raw.empty:
                    st.error("❌ Failed to scrape reviews.")
                    if hasattr(scraper, 'error_log') and scraper.error_log:
                        st.warning("🔍 Scraper Diagnostic Log Trace:")
                        for log in scraper.error_log:
                            st.markdown(f"- {log}")
                    st.stop()

                st.info("🧹 Processing & cleaning reviews data...")
                df_cleaned = clean_data(df_raw)

                st.info("🧠 Analyzing sentiment...")
                df_processed = analyze_sentiment(df_cleaned)

                save_to_db(df_processed)
                st.session_state.mode = "single"
                st.success(f"🎉 Success! Processed & saved {len(df_processed)} reviews from URL.")
                st.rerun()

    if reset_btn:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS reviews")
            conn.commit()
            conn.close()
            st.session_state.mode = None
            st.success("✅ Database cleared successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Reset failed: {e}")

# ----------------- TAB 2: DASHBOARD INSIGHTS -----------------
with tab_dash:
    try:
        df = load_data()
    except Exception:
        df = pd.DataFrame()

    if df.empty:
        st.info("ℹ️ No review data found in database. Go to the **Run Pipeline** tab to scrape data.")
    else:
        # Calculate summary values
        total_rev = len(df)
        avg_price = df["Price"].mean()
        avg_rating = df["Rating"].mean()
        
        pos_df = df[df["Sentiment"] == "POSITIVE"]
        neg_df = df[df["Sentiment"] == "NEGATIVE"]
        positive_count = len(pos_df)
        negative_count = len(neg_df)
        pos_ratio = positive_count / total_rev if total_rev > 0 else 0.0

        # KPI Metrics Row
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Reviews Scraped</div>
                <div class="metric-num">{total_rev}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Average Price</div>
                <div class="metric-num">₹{int(avg_price) if not pd.isna(avg_price) else 0}</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Average Rating</div>
                <div class="metric-num">{round(avg_rating, 2) if not pd.isna(avg_rating) else 0.0}★</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Positive Ratio</div>
                <div class="metric-num">{round(pos_ratio * 100, 1)}%</div>
            </div>
            """, unsafe_allow_html=True)

        # AI Recommendation banner
        is_recommended = pos_ratio >= 0.60
        decision_class = "decision-buy" if is_recommended else "decision-avoid"
        decision_icon = "✅" if is_recommended else "❌"
        decision_title = "RECOMMENDED (BUY)" if is_recommended else "NOT RECOMMENDED"
        decision_desc = (
            f"Based on AI sentiment analysis, **{round(pos_ratio*100, 1)}%** of reviews are positive ({positive_count} vs {negative_count}). "
            "Customers express high satisfaction. The product is recommended."
            if is_recommended else
            f"Based on AI sentiment analysis, only **{round(pos_ratio*100, 1)}%** of reviews are positive ({positive_count} vs {negative_count}). "
            "Negative feedback is high. We recommend avoiding or choosing an alternative."
        )

        st.markdown(f"""
        <div class="decision-card {decision_class}">
            <h3 style="margin-top:0; color:inherit;">{decision_icon} AI recommendation: {decision_title}</h3>
            <p style="font-size:1.05rem; margin-bottom:0; color:inherit;">{decision_desc}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Charts Section
        st.subheader("📊 Visual Analytics")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("#### Star Rating Distribution")
            df_ratings = df["Rating"].round().astype(int)
            rating_counts = df_ratings.value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
            chart_df = pd.DataFrame({"Reviews": rating_counts.values}, index=["1★", "2★", "3★", "4★", "5★"])
            st.bar_chart(chart_df, color="#4f46e5")

        with chart_col2:
            st.markdown("#### Sentiment Distribution")
            sent_counts = df["Sentiment"].value_counts().reindex(["POSITIVE", "NEGATIVE", "NEUTRAL"], fill_value=0)
            st.bar_chart(pd.DataFrame({"Reviews": sent_counts.values}, index=sent_counts.index), color="#db2777")

        # Multi product breakdown
        if st.session_state.mode == "multi":
            st.markdown("---")
            st.subheader("📦 Product Comparison")
            
            # Aggregate stats by product
            product_group = df.groupby("Product Name").agg({
                "Price": "mean",
                "Rating": "mean",
                "Comment": "count"
            }).rename(columns={"Comment": "Review Count"}).reset_index()

            st.dataframe(
                product_group.style.format({
                    "Price": "₹{:.0f}",
                    "Rating": "{:.2f}★",
                    "Review Count": "{:.0f}"
                }),
                use_container_width=True,
                hide_index=True
            )

# ----------------- TAB 3: REVIEW EXPLORER -----------------
with tab_reviews:
    try:
        df = load_data()
    except Exception:
        df = pd.DataFrame()

    if df.empty:
        st.info("ℹ️ No review data found in database. Go to the **Run Pipeline** tab to scrape data.")
    else:
        st.subheader("🔍 Search and Filter Stored Reviews")
        
        # Explorer controls
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            search_text = st.text_input("Search Comments keyword", "")
        with filter_col2:
            sent_choice = st.selectbox("Sentiment Filter", ["All", "POSITIVE", "NEGATIVE", "NEUTRAL"])
        with filter_col3:
            rating_choice = st.selectbox("Star Rating Filter", ["All", "5★", "4★", "3★", "2★", "1★"])

        # Filter database records
        filtered_df = df.copy()
        if search_text:
            filtered_df = filtered_df[filtered_df["Comment"].str.contains(search_text, case=False, na=False)]
        if sent_choice != "All":
            filtered_df = filtered_df[filtered_df["Sentiment"] == sent_choice]
        if rating_choice != "All":
            target_val = int(rating_choice[0])
            filtered_df = filtered_df[filtered_df["Rating"].round() == target_val]

        st.write(f"Matches found: **{len(filtered_df)}** reviews")
        st.markdown("---")

        # Display list of reviews
        if filtered_df.empty:
            st.warning("⚠️ No reviews matched the current filter criteria.")
        else:
            for _, row in filtered_df.head(40).iterrows():
                # Form stars
                r_val = int(round(row["Rating"])) if not pd.isna(row["Rating"]) else 0
                stars = "★" * r_val + "☆" * (5 - r_val)
                
                # Sentiment tag CSS class
                badge_style = "badge-positive" if row["Sentiment"] == "POSITIVE" else ("badge-negative" if row["Sentiment"] == "NEGATIVE" else "badge-neutral")
                
                st.markdown(f"""
                <div class="review-feed-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <span class="rating-stars">{stars}</span>
                            <span style="font-size: 0.85rem; color: #8E9CAE; margin-left: 12px; font-weight: 500;">
                                Price: ₹{int(row['Price']) if not pd.isna(row['Price']) else 'N/A'}
                            </span>
                        </div>
                        <span class="sentiment-badge {badge_style}">{row['Sentiment']}</span>
                    </div>
                    <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 6px; color: inherit; font-family: 'Outfit', sans-serif;">
                        {row['Product Name']}
                    </div>
                    <p style="font-size: 0.92rem; opacity: 0.85; margin: 0; line-height: 1.5; font-style: italic;">
                        "{row['Comment']}"
                    </p>
                </div>
                """, unsafe_allow_html=True)