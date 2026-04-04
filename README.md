# Myntra Product Review Analyzer 🛍️

---

## 📌 Problem Statement

E-commerce platforms contain vast amounts of unstructured review data. Businesses often struggle to extract meaningful insights related to product performance, pricing perception, and customer sentiment.

This project solves a **real B2B use case**:

> Enabling businesses to analyze product reviews and customer sentiment from Myntra in a structured and usable format.

---

## 💡 Solution Overview

An end-to-end **data engineering pipeline** that:

1. Scrapes product review data from Myntra
2. Cleans and standardizes the data
3. Stores it in a structured database
4. Provides a **dynamic dashboard** for insights

---

## 🌐 Live Application

👉 https://myntra-review-scrapper-aj3w.onrender.com

---

## 🚀 Key Features

* 🔍 Search products dynamically
* 🌐 Analyze product via URL
* 📊 Product-level insights (price, rating)
* 💬 Positive & negative review extraction
* 🧹 Automated data cleaning
* 💾 Data storage in SQLite & CSV
* 🔄 Reset and rerun pipeline

---

## ⚙️ Tech Stack

* **Python**
* **Selenium + BeautifulSoup** (data scraping)
* **Pandas** (data processing)
* **SQLite** (data storage)
* **Streamlit** (dashboard)
* **Render** (deployment)

---

## 🧠 Architecture

```
Scraper (Selenium + BS4)
        ↓
Data Cleaning (Pandas)
        ↓
Storage (SQLite / CSV)
        ↓
Dashboard (Streamlit)
```

---

## 🔄 Data Pipeline Details

### 1. Scraper

* Extracts product URLs and reviews
* Handles:

  * Pagination
  * Missing fields
  * Dynamic content

### 2. Data Cleaning

* Cleans price and rating values
* Converts data into structured numeric format
* Removes invalid/missing entries

### 3. Storage

* Stores processed data in:

  * SQLite database
  * CSV file

### 4. Dashboard

* Interactive interface for users
* Displays:

  * Product insights
  * Average rating
  * Positive vs negative reviews

---

## ⚡ Automation

* Pipeline runs dynamically based on user input
* No manual preprocessing required
* Ensures consistent outputs

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

---

## ⚠️ Deployment Limitations & Design Decisions

### 🚫 Why Live Scraping is Disabled

The deployed application does not perform real-time scraping due to platform constraints:

* Render does not support full browser environments required by Selenium
* ChromeDriver and GUI-based automation are restricted
* Myntra may block automated scraping requests

---

### ✅ Adopted Solution (Production Approach)

To ensure reliability, the project follows a **decoupled architecture**:

```
Local Scraper → Cleaned Data → Database/CSV → Deployed Dashboard
```

* Scraping is performed locally
* Data is stored and reused
* Dashboard serves preprocessed data

---

### 🎯 Why This Approach is Better

* Ensures stable deployment
* Avoids browser dependency issues
* Improves performance
* Reflects real-world data engineering systems

---

## 🚧 Challenges Faced

* Python 3.14 compatibility issues
* Pandas build failures
* Selenium not supported in cloud environment

### ✅ Solutions

* Downgraded Python to 3.10
* Used compatible library versions
* Separated scraping from UI

---

## 🧠 Future Improvements

* Add sentiment analysis (ML/NLP)
* Automate scraping using scheduler
* Add charts and visualizations
* Use scalable database (PostgreSQL)
* Deploy scraper as a microservice

---

## 📦 Submission Notes

* Fully deployed working application
* Clean GitHub repository
* End-to-end pipeline implemented
* Business-focused solution

---

## 🙌 Conclusion

This project demonstrates the ability to:

* Identify a real-world problem
* Build a complete data pipeline
* Handle deployment challenges
* Deliver a production-ready solution

🚀 Ready for real-world data engineering tasks.
