<h1 align="center">🛍️ Myntra Product Review Analyzer</h1>

<p align="center">
AI-powered system for scraping, analyzing, and recommending products using Transformer-based NLP
</p>

<hr>

<h2>📌 Problem</h2>
<p>
E-commerce platforms generate massive amounts of <b>unstructured review data</b>, making it difficult to evaluate product quality and customer sentiment efficiently.
</p>

<hr>

<h2>💡 Solution</h2>
<p>
Developed an <b>end-to-end AI pipeline</b> that:
</p>
<ul>
  <li>Scrapes product reviews from Myntra</li>
  <li>Cleans and processes raw data</li>
  <li>Applies <b>DistilBERT (Transformer NLP)</b> for sentiment analysis</li>
  <li>Stores structured data in a database</li>
  <li>Generates <b>Buy / Not Buy</b> recommendations</li>
</ul>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li>🔍 Dynamic product search</li>
  <li>🌐 Product analysis via URL</li>
  <li>🧠 Transformer-based sentiment analysis</li>
  <li>📊 Product insights (price, rating)</li>
  <li>💬 Positive & negative review classification</li>
  <li>🤖 AI recommendation system</li>
  <li>🔄 Reset & re-run pipeline</li>
  <li>🌐 Flask API support</li>
</ul>

<hr>

<h2>🧠 Architecture</h2>

<pre>
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
</pre>

<hr>

<h2>⚙️ Tech Stack</h2>
<ul>
  <li><b>Python</b></li>
  <li><b>Selenium + BeautifulSoup</b></li>
  <li><b>Pandas, NumPy</b></li>
  <li><b>Transformers (DistilBERT)</b></li>
  <li><b>SQLite</b></li>
  <li><b>Streamlit</b></li>
  <li><b>Flask</b></li>
</ul>

<hr>

<h2>📊 AI Recommendation Logic</h2>

<pre>
If Positive Reviews ≥ 60% → ✅ Recommended (Buy)
Else → ❌ Not Recommended
</pre>

<hr>

<h2>▶️ Run Locally</h2>

<pre>
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
</pre>





<hr>

<h2>⭐ Key Highlights</h2>
<ul>
  <li>End-to-end pipeline (Scraping → NLP → Recommendation)</li>
  <li>Uses Transformer-based NLP (DistilBERT)</li>
  <li>Real-world application</li>
  <li>Dashboard + API integration</li>
</ul>

<hr>

<p align="center">
⭐ If you found this useful, consider giving a star!
</p>
