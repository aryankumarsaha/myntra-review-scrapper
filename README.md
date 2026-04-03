# Myntra Product Review Analyzer 🛍️

## 📌 Problem
E-commerce platforms contain large amounts of unstructured review data. Businesses need a way to analyze product performance and customer sentiment.

---

## 💡 Solution
Built a dynamic data pipeline that:
- Scrapes product reviews from Myntra
- Cleans and processes the data
- Stores it in a database
- Displays insights using an interactive dashboard

---

## 🚀 Features
- 🔍 Search products dynamically
- 🌐 Analyze product via URL
- 📊 Product-level insights
- 💬 Positive & negative reviews
- 🔄 Reset and re-run pipeline

---

## ⚙️ Tech Stack
- Python
- Selenium + BeautifulSoup
- Pandas
- SQLite
- Streamlit

---

## 🧠 Architecture
Scraper → Cleaning → Database → Dashboard

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py