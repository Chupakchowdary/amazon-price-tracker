# Amazon Price Tracker

A simple Python project that checks prices of Amazon products and saves them into a CSV file.

## What it does
- Reads product URLs from `products.txt`
- Scrapes product name and price
- Saves all results into `amazon_prices.csv`
- Stores last known prices in the `last_prices` folder

## How to run
Install dependencies:
pip install -r requirements.txt

Run the script:
python amazon_scrape.py

Prices will be recorded in the CSV file automatically.
