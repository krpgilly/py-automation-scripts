# Grocery Price Comparison Tool

A Python-based project to scrape and compare grocery prices per 100g between Lidl and Tesco.

> **Project Status: Work in Progress (WIP)**  
> This project is in its early stages. The database schema and a Lidl scraping prototype are active, while the Tesco module is currently a structural placeholder.

---

## Current Project Structure

*`database/init_db.py` — Configures SQLite tables for stores, products, and historic prices.
*`scrapers/lidl_scraper.py` — Live Selenium prototype extracting real-time pricing data.
*`scrapers/tesco_scraper.py` — Structural blueprint and TODO notes for the Tesco selector engine.
*`main.py` — (Planned) Automation script to run both scrapers and normalise prices.

---

## Getting Started

### 1. Prerequisites

Install the required browser automation packages:

```bash
pip install selenium webdriver-manager
```

### 2. Initialise Database

Generate the local SQLite database container:

```bash
python database/init_db.py
```

### 3. Run the Lidl Prototype

Execute the working selector script:

```bash
python scrapers/lidl_scraper.py
```

---

## Next Steps / Roadmap

- [x] Design relational database schema (`products.db`)
- [x] Build functional Selenium selector prototype for Lidl
- [ ] Research Tesco anti-bot cookie wall workarounds
- [ ] Map out HTML selectors for Tesco regular and Clubcard pricing
- [ ] Code price normalization logic (converting items to price per 100g)
- [ ] Hook scrapers up to the SQLite database to save results automatically
