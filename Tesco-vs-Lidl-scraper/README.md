# Tesco vs Lidl Price Comparison

A Python scraper that pulls grocery prices from Tesco and Lidl, then normalizes everything to a single metric: price per 100g. Makes it easy to compare whether that tin of beans is actually cheaper at Lidl or if Tesco's just running a promotion.

## What This Does

Scrapes product pages from both supermarkets, grabs the raw price and weight, then calculates the real cost per 100g so you're not fooled by different package sizes. Stores everything in a local SQLite database—both the raw numbers and the computed values, so you can see exactly what the scraper found and how it was normalized.

---

## Key Engineering Decisions

### Fallback Selectors for Resilience

Web scraping is fragile. One HTML layout change on Tesco's site and your XPath selector stops working. So instead of betting everything on a single selector, each scraper tries multiple ones in order:

```python
price_selectors = [
    (By.CSS_SELECTOR, "p[class*='priceText']"),
    (By.CSS_SELECTOR, ".price-per-item"),
    (By.XPATH, "//span[contains(@class, 'actual-price')]")
]
```

The `find_price()` function walks through this list, waits up to 10 seconds for each one, and returns the first that actually appears on the page. If none work, it raises an error instead of silently returning garbage data.

### Normalize Edge Cases Handled

Real-world pricing data is messy. Weights come as "200g", "1.5kg", or "500mg". Prices might be "£2.50" or "45p". The `normalize_price()` function handles:

- Currency formats: "£" prefix or "p" suffix (converting pence to pounds)
- Weight units: grams, kilograms, milligrams—all converted to a single unit before calculation
- Spacing: `" £1.50 "` and `"£1.50"` both work
- Zero-weight protection: catches division errors before they happen
- Rounding: results rounded to 3 decimal places for consistency

The test suite catches regressions on these edge cases. When you normalize `"£2.00"` for `"200g"`, you get exactly `1.0` (£1.00 per 100g), not some float precision nightmare.

### Database Schema: Raw + Computed Values

The database keeps both raw and normalized prices:

```sql
CREATE TABLE prices (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    product_id INTEGER,
    
    raw_price TEXT,              -- What the scraper found: "£2.50"
    raw_unit_price TEXT,         -- What the scraper found: "£1.25/100g"
    price_per_100g REAL,         -- Computed normalized value
    
    scraped_at TEXT,
    
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

Why both? If normalization logic has a bug, you can always re-normalize using the raw data. Plus, you can audit exactly what the scraper saw versus what you computed.

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

- **selenium**: Browser automation library
- **webdriver-manager**: Automatically downloads and manages Chrome driver versions

### 3. Initialize the Database

```bash
python -m database.db
```

This creates `products.db` in the project root with the schema ready to go.

### 4. Run a Scraper

Lidl (currently working):

```bash
python -m scrapers.lidl_scraper
```

Tesco (structure in place, selectors still being tuned):

```bash
python -m scrapers.tesco_scraper
```

Both will print the found price and normalized price per 100g to the console.

### 5. Run All Scrapers + Compare

```bash
python main.py
```

This orchestrates the full pipeline (coming soon—currently it's just a TODO list).

---

## Project Structure

```
database/
  db.py              # Schema initialization
  normalize.py       # Price normalization logic + unit conversion

scrapers/
  find_price.py      # Fallback selector logic (the resilience layer)
  lidl_scraper.py    # Lidl-specific selectors and workflow
  tesco_scraper.py   # Tesco-specific selectors and workflow

tests/
  test_normalize.py  # Edge case tests for the normalize functions

main.py              # Entry point (orchestrates both scrapers)
```

---

## Planned JSON API

Right now, the scrapers print results to the console and store them in a SQLite database. The next step would be a simple HTTP API that:

- Serves comparison data as JSON
- Lets you query prices for a specific product across both stores
- Returns the historical trend (prices over time)

Why? Because:

1. **Accessibility**: A REST endpoint is easier to consume from other tools, scripts, or a web frontend than directly querying SQLite.
2. **Separation**: Scraping logic stays separate from serving logic. You can run scrapers on a schedule and keep the API running independently.
3. **Extensibility**: Once you have an API, adding a web frontend, mobile app, or integrations with shopping apps becomes straightforward.

Something like:

```
GET /api/compare?product=brie&store=lidl,tesco
→ {
    "product": "brie",
    "results": [
      {"store": "lidl", "price_per_100g": 0.82, "scraped_at": "2026-08-14T10:30:00"},
      {"store": "tesco", "price_per_100g": 0.95, "scraped_at": "2026-08-14T10:30:00"}
    ]
  }
```

For now, the raw SQLite queries work fine. But as the project grows, an API layer keeps things clean and flexible.

---

## Testing

Run the normalize tests to ensure edge cases stay handled:

```bash
python -m pytest tests/test_normalize.py -v
```

(Install pytest first: `pip install pytest`)

---

## Known Limitations & Next Steps

- **Tesco selectors**: Still being tuned—the HTML structure is more complex than Lidl's
- **No product matching**: Currently tests on hardcoded URLs; need to build a proper product search + matching workflow
- **No scheduling**: Prices are only fetched on-demand; a scheduled job (cron / APScheduler) would build historical trends
- **No frontend**: Data lives in the database—visualizing trends and comparisons needs a UI

---

## Why This Matters

Supermarket pricing isn't transparent. A 400g tin might be cheaper at one store, but an 800g bottle at another. By normalizing to per-100g, you cut through the packaging tricks and see what you're actually paying for. That's useful for budgeting, price tracking, and calling out when a store is just playing games with their portions.

- [ ] Research Tesco anti-bot cookie wall workarounds
- [ ] Map out HTML selectors for Tesco regular and Clubcard pricing
- [ ] Hook scrapers up to the SQLite database to save results automatically
