# TODO: open browser
# TODO: navigate to Tesco product page
# TODO: scrape product name
# TODO: scrape product price
# TODO: scrape product weight
# TODO: normalize price to £/100g
# TODO: return data

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.tesco.com/shop/en-GB/products/299914515"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

price_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "p[class*='priceText']"))
)
print("Price:", price_element.text)

driver.quit()
