from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import platform
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote

class ScrapeReviews:
    def __init__(self, product_name: str, no_of_products: int):
        self.error_log = []
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

        try:
            self.driver = webdriver.Chrome(options=options)
            
            # Override navigator.webdriver to prevent detection
            try:
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                })
            except Exception as cdp_err:
                self.error_log.append(f"⚠️ CDP command override failed: {cdp_err}")
        except Exception as driver_err:
            self.driver = None
            self.error_log.append(f"❌ Selenium Webdriver failed to initialize: {driver_err}")

        self.product_name = product_name
        self.no_of_products = no_of_products

    # -------------------------------
    # SCROLL FUNCTION
    # -------------------------------
    def scroll_page(self):
        if not self.driver:
            return
        try:
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 2000);")
                time.sleep(2)
        except Exception as e:
            self.error_log.append(f"⚠️ Error scrolling page: {e}")

    # -------------------------------
    # GET PRODUCT URLS
    # -------------------------------
    def scrape_product_urls(self, product_name):
        if not self.driver:
            self.error_log.append("❌ scrape_product_urls aborted: Webdriver is not initialized.")
            return []

        try:
            search_string = product_name.replace(" ", "-")
            encoded_query = quote(search_string)
            url = f"https://www.myntra.com/{search_string}?rawQuery={encoded_query}"
            
            print(f"[DEBUG] Navigating to search: {url}")
            self.driver.get(url)

            time.sleep(5)
            self.scroll_page()

            page_title = self.driver.title
            page_source = self.driver.page_source
            print(f"[DEBUG] Search page loaded. Title: '{page_title}'")

            soup = bs(page_source, "html.parser")
            product_urls = []

            for a in soup.find_all("a", href=True):
                if "/buy" in a["href"]:
                    product_urls.append(a["href"])

            if not product_urls:
                self.error_log.append(f"⚠️ No product links found on search page. Page title: '{page_title}' (Source length: {len(page_source)} chars)")
                # If cloudflare is visible
                if "cloudflare" in page_source.lower() or "challenge" in page_source.lower() or "denied" in page_title.lower():
                    self.error_log.append("🚨 Detected Cloudflare / Access Denied bot protection blockage!")

            return list(set(product_urls))[:self.no_of_products]
        except Exception as e:
            self.error_log.append(f"❌ Exception in scrape_product_urls: {e}")
            return []

    # -------------------------------
    # GET PRODUCT DETAILS
    # -------------------------------
    def extract_reviews(self, product_link):
        if not self.driver:
            self.error_log.append("❌ extract_reviews aborted: Webdriver is not initialized.")
            return None

        try:
            if product_link.startswith("http"):
                url = product_link
            else:
                url = "https://www.myntra.com/" + product_link.lstrip("/")
            
            print(f"[DEBUG] Navigating to product: {url}")
            self.driver.get(url)
            time.sleep(3)

            page_title = self.driver.title
            page_source = self.driver.page_source
            print(f"[DEBUG] Product page loaded. Title: '{page_title}'")

            soup = bs(page_source, "html.parser")

            title = soup.title.text if soup.title else "No Title"

            price_tag = soup.find("span", {"class": "pdp-price"})
            price = price_tag.text if price_tag else "0"

            review_link = soup.find("a", {"class": "detailed-reviews-allReviews"})

            if not review_link:
                self.error_log.append(f"⚠️ No detailed reviews link found for '{title}' (URL: {url}). Page title: '{page_title}'")
                if "cloudflare" in page_source.lower() or "challenge" in page_source.lower() or "denied" in page_title.lower():
                    self.error_log.append("🚨 Detected Cloudflare / Access Denied bot protection blockage on product page!")
                return None

            return {
                "title": title,
                "price": price,
                "review_link": review_link["href"],
            }
        except Exception as e:
            self.error_log.append(f"❌ Exception in extract_reviews: {e}")
            return None

    # -------------------------------
    # GET REVIEWS
    # -------------------------------
    def extract_products(self, product_data):
        if not self.driver:
            return pd.DataFrame()

        try:
            review_url = "https://www.myntra.com" + product_data["review_link"]
            print(f"[DEBUG] Navigating to reviews page: {review_url}")
            self.driver.get(review_url)

            time.sleep(3)
            self.scroll_page()

            page_title = self.driver.title
            page_source = self.driver.page_source

            soup = bs(page_source, "html.parser")

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

            if not data:
                self.error_log.append(f"⚠️ No user reviews found on page '{product_data['title']}'. Title: '{page_title}'")
                if "cloudflare" in page_source.lower() or "challenge" in page_source.lower() or "denied" in page_title.lower():
                    self.error_log.append("🚨 Detected Cloudflare / Access Denied bot protection blockage on reviews page!")

            return pd.DataFrame(data)

        except Exception as e:
            self.error_log.append(f"❌ Exception in extract_products: {e}")
            return pd.DataFrame()

    # -------------------------------
    # SCRAPE SINGLE PRODUCT
    # -------------------------------
    def scrape_single_product(self, product_url):
        try:
            product_data = self.extract_reviews(product_url)
            if not product_data:
                if self.driver:
                    self.driver.quit()
                return pd.DataFrame()

            df = self.extract_products(product_data)
            if self.driver:
                self.driver.quit()
            return df
        except Exception as e:
            self.error_log.append(f"❌ Exception in scrape_single_product: {e}")
            if self.driver:
                self.driver.quit()
            return pd.DataFrame()

    # -------------------------------
    # MAIN
    # -------------------------------
    def get_review_data(self):
        try:
            product_urls = self.scrape_product_urls(self.product_name)

            all_data = []

            for url in product_urls:
                product_data = self.extract_reviews(url)

                if product_data:
                    df = self.extract_products(product_data)

                    if not df.empty:
                        all_data.append(df)

            if self.driver:
                self.driver.quit()

            if not all_data:
                return pd.DataFrame()

            return pd.concat(all_data, ignore_index=True)
        except Exception as e:
            self.error_log.append(f"❌ Exception in get_review_data: {e}")
            if self.driver:
                self.driver.quit()
            return pd.DataFrame()