from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price
from scrapers.find_price import find_unit_price
from database.normalize import normalize_unit_price

def scrape_tesco():
    url = "https://www.tesco.com/shop/en-GB/products/299914515"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    price_selectors = [
        (By.CSS_SELECTOR, "p[class*='priceText']"),
        (By.CSS_SELECTOR, ".price-per-item"),
        (By.CSS_SELECTOR, "span[data-testid='value']"),
        (By.XPATH, "//span[contains(@class, 'actual-price')]")
    ]

    unit_price_selectors = [
    (By.CLASS_NAME, "online-components-product-tile-unit-price__subtext"),
    (By.CSS_SELECTOR, "p.online-components-product-tile-unit-price__subtext"),
    (By.XPATH, "//p[contains(@class, 'online-components-product-tile-unit-price__subtext')]"),
]

    try:
            price = find_price(driver, price_selectors, timeout=10)
            unit_price = find_unit_price(driver, unit_price_selectors, timeout=10)
            print(f"Found price:{price}")
            print(f"Found unit price: {unit_price}")
            return {
                "price": price,
                "price_per_100g": normalize_unit_price(unit_price)
            }

    except ValueError as e:
        print(f"tesco scraping failed: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_tesco()
    print(result)