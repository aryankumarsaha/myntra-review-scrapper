# Myntra Product Review Analyzer 🛍️

## 📌 Problem Statement

Businesses often lack structured insights from e-commerce platforms. Product reviews contain valuable signals about customer satisfaction, pricing perception, and product quality — but this data is unstructured and difficult to use.

This project solves a **real B2B use case**:

> Helping businesses analyze product performance and customer sentiment from Myntra reviews.

---

## 💡 Solution Overview

An end-to-end **data pipeline** that:

1. Collects product review data from Myntra
2. Cleans and standardizes the data
3. Stores it in a structured database
4. Provides a **dynamic dashboard** for business insights

---

## 🌐 Live Application

👉 **Try the app here:**
https://myntra-review-scrapper-aj3w.onrender.com

---

## 🚀 Key Features

* 🔍 Search products dynamically
* 🌐 Analyze a specific product via URL
* 📊 Product-level insights (price, average rating)
* 💬 Extract positive & negative reviews
* 🧹 Automated data cleaning pipeline
* 💾 Data stored in SQLite database
* 🔄 Reset and rerun pipeline dynamically

---

## ⚙️ Tech Stack

* **Python**
* **Selenium + BeautifulSoup** (data scraping)
* **Pandas** (data processing)
* **SQLite** (data storage)
* **Streamlit** (interactive dashboard)
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

* Extracts product data from Myntra
* Handles:

  * Multiple product links
  * Missing values
  * Dynamic pages

### 2. Data Cleaning

* Removes unwanted characters from price & ratings
* Converts data into structured numeric format
* Drops missing/invalid entries

### 3. Storage

* Cleaned data stored in:

  * SQLite database
  * CSV file for quick access

### 4. Dashboard (Business Interface)

* Interactive UI for users
* Displays:

  * Product insights
  * Average rating
  * Positive vs negative reviews

---

## ⚡ Automation

* Pipeline runs dynamically based on user input
* No manual data preprocessing required
* Ensures consistent and reliable outputs

---

## ▶️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run pipeline (scraping + cleaning + storage)
python main.py

# Run dashboard
streamlit run app/streamlit_app.py
```

---

## 📌 Assumptions & Design Decisions

* Limited to top reviews for performance
* SQLite chosen for lightweight storage
* Separated scraping and UI to ensure smooth deployment

---

## 🚧 Challenges Faced

* Dependency issues with Python 3.14
* Pandas build failures
* Selenium incompatibility with deployment

✅ Resolved by:

* Downgrading Python to 3.10
* Using compatible library versions
* Decoupling scraper from UI

---

## 🧠 Future Improvements

* Add sentiment analysis (ML/NLP)
* Automate scraping using scheduler
* Add visualization charts
* Scale database (PostgreSQL / cloud DB)

---

## 📦 Submission Notes

* Fully functional deployed application
* Clean GitHub repository
* End-to-end data pipeline implemented
* Business-focused use case demonstrated

---

## 🙌 Conclusion

This project demonstrates the ability to:

* Identify a real-world problem
* Build a scalable data pipeline
* Deploy a working solution
* Deliver business-ready insights

🚀 Ready for real-world data engineering tasks.
