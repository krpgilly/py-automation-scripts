from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def find_price(driver, selectors, timeout=10):
    """
    selectors: a list of tuples like (By.CSS_SELECTOR, "p[class*='priceText']")
    Tries each one in order. Returns the text of the first one that's found.
    Raises an exception if none of them work.
    """
    for by, sel in selectors:
        try:
            price_element = WebDriverWait(driver, timeout).until(
                   EC.presence_of_element_located((by, sel))
            )
            
            return price_element.text.strip()
            
        except TimeoutException:
            continue
    
    raise ValueError(f"None of the selectors worked: {selectors}")

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