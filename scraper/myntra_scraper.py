from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import platform
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapeReviews:
    def __init__(self, product_name: str, no_of_products: int):
        options = Options()
        
        # Automatically configure headless mode on cloud Linux deployments
        if platform.system() == "Linux":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.binary_location = "/usr/bin/chromium"
        else:
            options.add_argument("--start-maximized")

        # Bypass automated browser detection (Cloudflare / Akamai)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=options)
        
        # Override navigator.webdriver to prevent detection
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
        except Exception:
            pass

        self.product_name = product_name
        self.no_of_products = no_of_products

    # -------------------------------
    # SCROLL FUNCTION
    # -------------------------------
    def scroll_page(self):
        for _ in range(3):
            self.driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(2)

    # -------------------------------
    # GET PRODUCT URLS
    # -------------------------------
    def scrape_product_urls(self, product_name):
        search_string = product_name.replace(" ", "-")
        encoded_query = quote(search_string)

        self.driver.get(f"https://www.myntra.com/{search_string}?rawQuery={encoded_query}")

        time.sleep(5)
        self.scroll_page()

        soup = bs(self.driver.page_source, "html.parser")

        product_urls = []

        for a in soup.find_all("a", href=True):
            if "/buy" in a["href"]:
                product_urls.append(a["href"])

        return list(set(product_urls))[:self.no_of_products]

    # -------------------------------
    # GET PRODUCT DETAILS
    # -------------------------------
    def extract_reviews(self, product_link):
        try:
            if product_link.startswith("http"):
                url = product_link
            else:
                url = "https://www.myntra.com/" + product_link.lstrip("/")
            self.driver.get(url)
            time.sleep(3)

            soup = bs(self.driver.page_source, "html.parser")

            title = soup.title.text if soup.title else "No Title"

            price_tag = soup.find("span", {"class": "pdp-price"})
            price = price_tag.text if price_tag else "0"

            review_link = soup.find("a", {"class": "detailed-reviews-allReviews"})

            if not review_link:
                return None

            return {
                "title": title,
                "price": price,
                "review_link": review_link["href"],
            }
        except:
            return None

    # -------------------------------
    # GET REVIEWS
    # -------------------------------
    def extract_products(self, product_data):
        try:
            review_url = "https://www.myntra.com" + product_data["review_link"]
            self.driver.get(review_url)

            time.sleep(3)
            self.scroll_page()

            soup = bs(self.driver.page_source, "html.parser")

            reviews = soup.find_all("div", {"class": "detailed-reviews-userReviewsContainer"})

            data = []

            for review in reviews:
                rating_tag = review.find("span", class_="user-review-starRating")
                comment_tag = review.find("div", class_="user-review-reviewTextWrapper")

                data.append({
                    "Product Name": product_data["title"],
                    "Price": product_data["price"],
                    "Rating": rating_tag.text if rating_tag else "0",
                    "Comment": comment_tag.text if comment_tag else "No Comment"
                })

            return pd.DataFrame(data)

        except:
            return pd.DataFrame()

    # -------------------------------
    # SCRAPE SINGLE PRODUCT
    # -------------------------------
    def scrape_single_product(self, product_url):
        try:
            product_data = self.extract_reviews(product_url)
            if not product_data:
                self.driver.quit()
                return pd.DataFrame()

            df = self.extract_products(product_data)
            self.driver.quit()
            return df
        except:
            self.driver.quit()
            return pd.DataFrame()

    # -------------------------------
    # MAIN
    # -------------------------------
    def get_review_data(self):
        product_urls = self.scrape_product_urls(self.product_name)

        all_data = []

        for url in product_urls:
            product_data = self.extract_reviews(url)

            if product_data:
                df = self.extract_products(product_data)

                if not df.empty:
                    all_data.append(df)

        self.driver.quit()

        if not all_data:
            return pd.DataFrame()

        return pd.concat(all_data, ignore_index=True)