import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price
from scrapers.find_price import find_unit_price
from database.normalize import normalize_unit_price

load_dotenv()

def scrape_lidl():
    url = "https://www.lidl.co.uk/p/milbona-brie/p10045855"
   
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    price_selectors = [
        (By.CLASS_NAME, "ods-price__value"),
        (By.CSS_SELECTOR, "span[data-testid='value']"),
        (By.XPATH, "//span[contains(@class, 'price')]")
    ]

    unit_price_selectors = [
        (By.CLASS_NAME, "ods-price__footer"),
        (By.CSS_SELECTOR, "div.ods-price__footer"),
        (By.XPATH, "//div[contains(@class, 'ods-price__footer')]"),
    ]
    
    try:
        price = find_price(driver, price_selectors, timeout=10)
        unit_price = find_unit_price(driver, unit_price_selectors, timeout=10)
        print(f"Found price:{price}")
        print(f"Found unit price: {unit_price}")
        return {
            "price": price,
            "raw_unit_price": unit_price,
            "price_per_100g": normalize_unit_price(unit_price)
        }

    except ValueError as e:
        print(f"lidl scraping failed: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_lidl()
    print(result)