import sqlite3

from scrapers.tesco_scraper import scrape_tesco
from scrapers.lidl_scraper import scrape_lidl
from database.db import init_db, insert_price


def main():
    # Initialize the database
    init_db()

    # scrape TESCO
    tesco_result = scrape_tesco()
    if tesco_result:
        conn = sqlite3.connect("products.db")
        insert_price(conn, "Tesco", "Brie", tesco_result)
        conn.close()

    # scrape LIDL
    lidl_result = scrape_lidl()
    if lidl_result:
        conn = sqlite3.connect("products.db")
        insert_price(conn, "Lidl", "Brie", lidl_result)
        conn.close()

if __name__ == "__main__":
    main()