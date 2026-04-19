🛍️ Myntra Product Review Analyzer (AI-Powered)
📌 Problem

E-commerce platforms generate large volumes of unstructured customer reviews, making it difficult for users and businesses to quickly assess product quality and sentiment.

💡 Solution

Built an end-to-end AI-powered data pipeline that:

Scrapes product reviews from Myntra
Cleans and processes raw data
Applies transformer-based NLP (DistilBERT) for sentiment analysis
Stores structured data in a database
Generates intelligent product recommendations (Buy / Not Buy)
Visualizes insights via an interactive dashboard

🚀 Features
🔍 Dynamic product search using keywords
🌐 Single product analysis via URL
🧠 Sentiment analysis using DistilBERT (Transformer NLP)
📊 Product-level insights (price, rating, reviews)
💬 Positive & negative review classification
🤖 AI-based recommendation system (Buy / Not Buy)
🔄 Reset and re-run pipeline
🌐 Flask API for programmatic access


🧠 Architecture
User Input (Search / URL)
        ↓
Scraper (Selenium + BeautifulSoup)
        ↓
Raw Data (Product Name, Price, Rating, Comment)
        ↓
Data Cleaning (Pandas)
        ↓
NLP (DistilBERT Sentiment Analysis)
        ↓
Database (SQLite)
        ↓
Aggregation + Decision Engine
        ↓
Dashboard (Streamlit) + API (Flask)


⚙️ Tech Stack
Programming: Python
Web Scraping: Selenium, BeautifulSoup
Data Processing: Pandas, NumPy
NLP: Transformers (DistilBERT)
Database: SQLite
Visualization/UI: Streamlit
API: Flask

📊 AI Logic (Recommendation Engine)
Classifies each review as POSITIVE or NEGATIVE
Computes overall sentiment ratio
Generates decision:
If Positive Reviews ≥ 60% → ✅ Recommended (Buy)
Else → ❌ Not Recommended


▶️ Run Locally
# Install dependencies
pip install -r requirements.txt

# Run pipeline (scraping + NLP + DB)
python main.py

# Launch dashboard
streamlit run app/streamlit_app.py


🧠 Key Highlights
End-to-end data pipeline + AI integration
Uses transformer-based NLP (industry standard)
Combines scraping + ML + dashboard + API
Designed for real-world product decision-making
