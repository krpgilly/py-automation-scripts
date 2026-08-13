from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price


def scrape_tesco():
    url = "https://www.tesco.com/shop/en-GB/products/299914515"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    selectors = [
        (By.CSS_SELECTOR, "p[class*='priceText']"),
        (By.CSS_SELECTOR, ".price-per-item"),
        (By.CSS_SELECTOR, "span[data-testid='value']"),
        (By.XPATH, "//span[contains(@class, 'actual-price')]")
    ]

    try:
        price = find_price(driver, selectors, timeout=10)
        print(f"Found price:{price}")
        return price

    except ValueError as e:
        print(f"tesco scraping failed: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_tesco()
    print(result)