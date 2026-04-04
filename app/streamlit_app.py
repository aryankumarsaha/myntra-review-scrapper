




# .\venv\Scripts\activate
# streamlit run app/streamlit_app.py



import streamlit as st
import sys
import os
import pandas as pd

# Fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import load_data, save_to_db
from processing.clean_data import clean_data

st.set_page_config(page_title="Myntra Dashboard", layout="wide")

st.title("🛍️ Myntra Product Analyzer")

# -------------------------------
# SESSION STATE
# -------------------------------
if "mode" not in st.session_state:
    st.session_state.mode = None

# -------------------------------
# INPUTS (now just for UI)
# -------------------------------
product_input = st.text_input("🔎 Search Product (demo only)", "shoes")
url_input = st.text_input("🔗 Paste Product URL (demo only)")

col1, col2, col3 = st.columns(3)

with col1:
    search_btn = st.button("🔍 Load Products")

with col2:
    url_btn = st.button("🌐 Load from URL")

with col3:
    reset_btn = st.button("🔄 Reset")

# -------------------------------
# RESET
# -------------------------------
if reset_btn:
    st.session_state.mode = None
    st.experimental_rerun()

# -------------------------------
# LOAD DATA (NO SCRAPING)
# -------------------------------
if search_btn or url_btn:
    with st.spinner("Loading data..."):
        df = pd.read_csv("data.csv")   # 🔥 MAIN CHANGE
        df = clean_data(df)
        save_to_db(df)

        st.session_state.mode = "multi"
        st.success("✅ Data loaded!")

# -------------------------------
# DISPLAY
# -------------------------------
if st.session_state.mode:

    df = load_data()

    st.subheader("📦 Product-wise Insights")

    product_df = df.groupby("Product Name").agg({
        "Price": "mean",
        "Rating": "mean"
    }).reset_index()

    for product in product_df["Product Name"]:

        st.markdown(f"### 🛍️ {product}")

        product_reviews = df[df["Product Name"] == product]

        avg_rating = round(product_reviews["Rating"].mean(), 2)
        price = product_reviews["Price"].iloc[0]

        st.write(f"💰 Price: ₹{price}")
        st.write(f"⭐ Avg Rating: {avg_rating}")

        # Positive reviews
        st.write("🟢 Positive Reviews:")
        positive = product_reviews[product_reviews["Rating"] >= 4]
        for comment in positive["Comment"]:
            st.write(f"✔ {comment}")

        # Negative reviews
        st.write("🔴 Negative Reviews:")
        negative = product_reviews[product_reviews["Rating"] <= 2]
        for comment in negative["Comment"]:
            st.write(f"❌ {comment}")

        st.markdown("---")


# import streamlit as st
# import sys
# import os
# import pandas as pd

# # Fix path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from database.db import load_data, save_to_db
# from scraper.myntra_scraper import ScrapeReviews
# from processing.clean_data import clean_data

# st.set_page_config(page_title="Myntra Dashboard", layout="wide")

# st.title("🛍️ Myntra Product Analyzer")

# # -------------------------------
# # SESSION STATE
# # -------------------------------
# if "mode" not in st.session_state:
#     st.session_state.mode = None

# # -------------------------------
# # INPUTS
# # -------------------------------
# product_input = st.text_input("🔎 Search Product", "shoes")
# url_input = st.text_input("🔗 Paste Product URL")

# col1, col2, col3 = st.columns(3)

# with col1:
#     search_btn = st.button("🔍 Search Products")

# with col2:
#     url_btn = st.button("🌐 Fetch from URL")

# with col3:
#     reset_btn = st.button("🔄 Reset")

# # -------------------------------
# # RESET
# # -------------------------------
# if reset_btn:
#     st.session_state.mode = None
#     st.experimental_rerun()

# # -------------------------------
# # MULTI PRODUCT MODE
# # -------------------------------
# if search_btn:
#     with st.spinner("Scraping products..."):
#         scraper = ScrapeReviews(product_input, 3)
#         df = scraper.get_review_data()

#         df = clean_data(df)
#         save_to_db(df)

#         st.session_state.mode = "multi"
#         st.success("✅ Products fetched!")

# # -------------------------------
# # URL MODE
# # -------------------------------
# if url_btn and url_input:
#     with st.spinner("Fetching product..."):
#         scraper = ScrapeReviews("", 1)
#         df = scraper.scrape_single_product(url_input)

#         df = clean_data(df)
#         save_to_db(df)

#         st.session_state.mode = "single"
#         st.success("✅ Product fetched!")

# # -------------------------------
# # DISPLAY
# # -------------------------------
# if st.session_state.mode:

#     df = load_data()

#     # -------------------------------
#     # SINGLE PRODUCT
#     # -------------------------------
#     if st.session_state.mode == "single":

#         st.subheader("🛍️ Product Details")

#         product_name = df["Product Name"].iloc[0]
#         price = df["Price"].iloc[0]
#         avg_rating = round(df["Rating"].mean(), 2)

#         st.write(f"### {product_name}")
#         st.write(f"💰 Price: ₹{price}")
#         st.write(f"⭐ Avg Rating: {avg_rating}")

#         # Positive & Negative Reviews
#         positive = df[df["Rating"] >= 4]
#         negative = df[df["Rating"] <= 2]

#         st.subheader("🟢 Positive Reviews")
#         for comment in positive["Comment"]:
#             st.write(f"✔ {comment}")

#         st.subheader("🔴 Negative Reviews")
#         for comment in negative["Comment"]:
#             st.write(f"❌ {comment}")

#     # -------------------------------
#     # MULTI PRODUCT
#     # -------------------------------
#     elif st.session_state.mode == "multi":

#         st.subheader("📦 Product-wise Insights")

#         product_df = df.groupby("Product Name").agg({
#             "Price": "mean",
#             "Rating": "mean"
#         }).reset_index()

#         for product in product_df["Product Name"]:

#             st.markdown(f"### 🛍️ {product}")

#             product_reviews = df[df["Product Name"] == product]

#             avg_rating = round(product_reviews["Rating"].mean(), 2)
#             price = product_reviews["Price"].iloc[0]

#             st.write(f"💰 Price: ₹{price}")
#             st.write(f"⭐ Avg Rating: {avg_rating}")

#             # Positive reviews
#             st.write("🟢 Positive Reviews:")
#             positive = product_reviews[product_reviews["Rating"] >= 4]
#             for comment in positive["Comment"]:
#                 st.write(f"✔ {comment}")

#             # Negative reviews
#             st.write("🔴 Negative Reviews:")
#             negative = product_reviews[product_reviews["Rating"] <= 2]
#             for comment in negative["Comment"]:
#                 st.write(f"❌ {comment}")

#             st.markdown("---")