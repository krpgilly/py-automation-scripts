from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def scrape_lidl():
    
    url = "https://www.lidl.co.uk/p/milbona-brie/p10045855"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    price_element = driver.find_element(By.CLASS_NAME, "ods-price__value")
    price = price_element.text.strip()

    driver.quit()
    return price
