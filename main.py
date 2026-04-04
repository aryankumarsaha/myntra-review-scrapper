from scraper.myntra_scraper import ScrapeReviews
from processing.clean_data import clean_data
from database.db import save_to_db

def run_pipeline():
    print("Starting pipeline...")

    scraper = ScrapeReviews("shoes", 3)
    df = scraper.get_review_data()

    print("Scraping done ✅")

    df = clean_data(df)
    print("Cleaning done ✅")

    save_to_db(df)
    print("Saved to database ✅")

    print("Pipeline completed 🚀")

if __name__ == "__main__":
    run_pipeline()

# from scraper.myntra_scraper import ScrapeReviews
# from processing.clean_data import clean_data
# from database.db import save_to_db

# def run_pipeline():
#     print("Starting pipeline...")

#     scraper = ScrapeReviews("shoes", 3)
#     df = scraper.get_review_data()

#     print("Scraping done ✅")

#     df = clean_data(df)
#     print("Cleaning done ✅")

#     save_to_db(df)
#     print("Saved to database ✅")

#     print("Pipeline completed 🚀")

# if __name__ == "__main__":
#     run_pipeline()