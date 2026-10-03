# Tesco vs Sainsburys Price Comparison

A beginner-friendly Python project that compares supermarket prices by converting each product to a common value: price per 100g. That lets you compare Tesco and Sainsburys fairly, even when the products come in different weights or pack sizes.

This keeps the comparison focused on actual value rather than marketing pack size.

## What This Does

The project scrapes product data from Tesco and Sainsburys, extracts the raw price and item weight, and normalizes the result into one metric: price per 100g.

That makes it easier to see which supermarket is offering better value for the same product, even when the packaging is different.

The app also stores the results in a local SQLite database so both the raw scraped values and the normalized values are saved. This makes it easy to review the source data and the calculated value side by side.

---

## What Is Working Now

The main workflow is working through `main.py`.

When you run it, the app:

- creates or updates the database tables
- pulls data from the Tesco scraper
- pulls data from the Sainsburys scraper
- stores each result in SQLite
- saves the raw price, unit price, normalized price, and timestamp

This means the app is a working pipeline that collects supermarket data and stores it in a structured way.

---

## Key Engineering Decisions

### Fallback Selectors for Resilience

Web scraping is fragile. A tiny change in a website layout can break a selector. To make the scrapers more reliable, each one tries a few possible selectors instead of relying on a single one.

```python
price_selectors = [
    (By.CSS_SELECTOR, "p[class*='priceText']"),
    (By.CSS_SELECTOR, ".price-per-item"),
    (By.XPATH, "//span[contains(@class, 'actual-price')]")
]
```

The `find_price()` function checks each option in order and uses the first one that works. If none match, it raises a useful error instead of returning bad data quietly.

### Normalize Edge Cases Handled

Real supermarket data is messy. Some weights are shown as "200g", some as "1.5kg", and prices may be written as "£2.50" or "45p". The `normalize_price()` logic handles these cases:

- currency values like "£" and "p"
- weight units like grams, kilograms, and milligrams
- spacing issues like " £1.50 " and "£1.50"
- zero-weight protection to prevent division errors
- rounding for clean, consistent results

This is important because the comparison should be fair. If you normalize correctly, a 200g item and a 1kg item can be compared properly.

### Database Schema: Raw + Computed Values

The database keeps both the original scraped values and the calculated values:

```sql
CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER,
    product_id INTEGER,

    raw_price TEXT,
    raw_unit_price TEXT,
    price_per_100g REAL,

    scraped_at TEXT,

    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

This is helpful because if the normalization logic changes later, the original scraped values remain available. You can always recalculate and compare old data without losing the source information.

---

## Setup & Running

### Prerequisites

You need Python 3.7+ and pip.

### 1. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

On Mac/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install selenium webdriver-manager
```

- **selenium**: browser automation for scraping pages
- **webdriver-manager**: downloads and manages the correct Chrome driver automatically

### 3. Initialize the Database

```bash
python -m database.db
```

This creates `products.db` in the project root and sets up the tables for stores, products, and prices.

### 4. Run the Project

```bash
python main.py
```

This is the main entry point. It runs the scraping flow, saves data to SQLite, and updates the current price comparison data.

If you want to run an individual scraper manually, the project still supports that pattern too.

---

## Project Structure

```text
database/
  db.py              # database setup and insert logic
  normalize.py       # price normalization and unit conversion

scrapers/
  find_price.py      # selector fallback logic
  sainsburys_scraper.py  # Sainsburys scraper
  tesco_scraper.py   # Tesco scraper

tests/
  test_database.py   # checks that stores, products, and price data are saved correctly
  test_normalize.py  # checks for edge cases in the price calculation
  test_selector.py   # validates the Tesco and Sainsburys HTML selectors used by the scrapers

main.py              # main app entry point; works and stores results
README.md            # project overview
```

---

## Planned JSON API

The basic idea behind the project is still the same: collect prices from supermarkets, normalize them, and make the comparison easy to use.

The next useful step is a simple JSON API that exposes the saved data in a clean format.

This would let you:

- return product comparison data as JSON
- query prices across both stores for one item
- see historical price changes over time

Why this is a good next step:

1. **Accessibility**: JSON is easier for scripts, apps, and websites to consume than reading SQLite directly.
2. **Separation**: the scraper can keep doing its job while the API simply serves the stored results.
3. **Extensibility**: once the data is in JSON, it is easier to build a small frontend or a more advanced product tracker later.

An example of the kind of output we want:

```bash
GET /api/compare?product=brie&store=sainsburys,tesco
→ {
    "product": "brie",
    "results": [
      {"store": "sainsburys", "price_per_100g": 0.82, "scraped_at": "2026-08-14T10:30:00"},
      {"store": "tesco", "price_per_100g": 0.95, "scraped_at": "2026-08-14T10:30:00"}
    ]
  }
```

This is still a future step, but it fits the same project scope: the scraper gathers the numbers, the database stores them, and the API would just make them easier to use.

---

## Testing

Run the tests to check both the price conversion logic and the database insert workflow:

```bash
python -m pytest tests/ -v
```

The database test uses an in-memory SQLite database, so it checks that:

- store and product records are created
- raw price and unit price values are saved
- the normalized price per 100g is saved
- a scrape timestamp is added

The normalize tests check the price conversion logic, including different currency and weight formats, invalid values, and zero-weight protection.

The selector tests validate the scraper configuration itself by checking that the Tesco and Sainsburys product selectors are valid CSS selectors and that the product name and price selectors are set up correctly for each store. This helps catch broken selectors early before the scraper tries to parse the page.

If needed, install pytest first:

```bash
pip install pytest
```

---

## Current Status & Next Steps

The project is now in a stronger position than before:

- `main.py` is working and runs the pipeline
- the database schema is storing products, stores, and prices separately
- the comparison logic is tied to real saved data
- the JSON API is still the next natural layer to build on top of that data

Possible future improvements include:

- better Tesco and Sainsburys selectors and anti-bot handling
- product matching for more than hardcoded examples
- scheduled scraping for price history
- a simple frontend or API dashboard

---

## Why This Matters

Supermarket pricing can be confusing. A product can look cheap because of its pack size, but the real value is in the price per 100g. This project makes that comparison easier and more transparent.

It is useful for budgeting, checking value, and understanding whether supermarkets are making the real cost harder to compare.
