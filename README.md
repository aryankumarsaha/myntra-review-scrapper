# Myntra Product Review Analyzer 🛍️

---

## 📌 Problem Statement

E-commerce platforms generate a massive amount of unstructured customer review data. Businesses often struggle to extract meaningful insights such as customer sentiment, product performance, and pricing perception from this data.

This project addresses a **real B2B use case**:

> Enabling businesses to transform unstructured review data into structured insights for better decision-making.

---

## 💡 Solution Overview

This project implements an end-to-end **data engineering pipeline** that:

1. Scrapes product and review data from Myntra
2. Cleans and standardizes the raw data
3. Stores processed data in a structured format
4. Provides an interactive dashboard for analysis

---

## 🌐 Live Application

👉 https://myntra-review-scrapper-aj3w.onrender.com

---

## 🚀 Key Features

* 🔍 Search and analyze products
* 🌐 URL-based product analysis
* 📊 Product-level insights (price, rating)
* 💬 Positive & negative review extraction
* 🧹 Data cleaning and preprocessing pipeline
* 💾 Storage using SQLite & CSV
* 🔄 Reset and rerun functionality

---

## ⚙️ Tech Stack

* **Python**
* **Selenium + BeautifulSoup** (scraping)
* **Pandas** (data processing)
* **SQLite** (storage)
* **Streamlit** (dashboard)
* **Render** (deployment)

---

## 🧠 Architecture

```id="arch001"
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

* Extracts product links, ratings, and reviews
* Handles:

  * Multiple product pages
  * Missing fields
  * Dynamic content

### 2. Data Cleaning

* Removes non-numeric characters from price and ratings
* Converts values into structured numeric format
* Drops invalid or missing entries

### 3. Storage

* Cleaned data is stored in:

  * SQLite database
  * CSV file

### 4. Dashboard (Business Interface)

* Interactive UI built with Streamlit
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

```bash id="run001"
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

---

## ⚠️ Deployment Limitations & Design Decisions

### 🚫 Why Selenium is Not Used in the Deployed Application

Selenium requires a full browser environment to operate:

```text id="flow001"
Python → Selenium → ChromeDriver → Chrome Browser
```

However, cloud platforms like Render have the following constraints:

* ❌ No GUI (graphical interface) support
* ❌ No pre-installed browser (Chrome/Firefox)
* ❌ No browser drivers (ChromeDriver)
* ❌ Restricted system-level access
* ❌ Limited CPU and memory

Even in headless mode, Selenium still requires browser binaries and drivers, which are not available in such environments.

---

### 🚀 Adopted Solution (Production-Oriented Design)

To ensure reliability, the architecture was redesigned:

```text id="flow002"
Local Scraper → Cleaned Data → Database/CSV → Deployed Dashboard
```

* Scraping is performed locally or offline
* Cleaned data is stored and reused
* The deployed dashboard reads preprocessed data

---

### 🎯 Why This Approach is Better

* ✅ Ensures stable deployment
* ✅ Avoids browser dependency issues
* ✅ Improves performance
* ✅ Follows real-world data engineering practices

---

## 🚧 Challenges Faced

* Python 3.14 compatibility issues
* Pandas and Pillow build failures
* Selenium not supported in deployment

### ✅ Solutions Implemented

* Downgraded Python to 3.10
* Updated library versions for compatibility
* Separated scraping from UI layer

---

## 🧠 Future Improvements

* Add sentiment analysis (NLP/ML)
* Automate scraping using schedulers (cron/Airflow)
* Add data visualizations and charts
* Use scalable database (PostgreSQL)
* Deploy scraper as a separate microservice

---

## 📦 Submission Notes

* Fully deployed working application
* Clean and structured GitHub repository
* End-to-end pipeline implemented
* Business-focused solution

---

## 🙌 Conclusion

This project demonstrates the ability to:

* Identify a real-world business problem
* Build an end-to-end data pipeline
* Handle deployment challenges effectively
* Deliver a scalable and production-ready solution

🚀 Ready for real-world data engineering tasks.
