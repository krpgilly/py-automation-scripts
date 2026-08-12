from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers.find_price import find_price

def scrape_lidl():
    url = "https://www.lidl.co.uk/p/milbona-brie/p10045855"
   
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    selectors = [
        (By.CLASS_NAME, "ods-price__value"),
        (By.CSS_SELECTOR, "span[data-testid='value']"),
        (By.XPATH, "//span[contains(@class, 'price')]")
    ]

    
    try:
        price = find_price(driver, selectors, timeout=10)
        print(f"Found price:{price}")
        return price

    except ValueError as e:
        print(f"lidl scraping failed: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_lidl()
    print(result)