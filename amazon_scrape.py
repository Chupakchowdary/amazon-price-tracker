import requests
from bs4 import BeautifulSoup
import json
import csv
import os
from datetime import datetime
from email_alert import send_email

# Load all product URLs
with open("products.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/15.0 Mobile/15E148 Safari/604.1"
    )
}

# Store last prices per product
if not os.path.exists("last_prices"):
    os.makedirs("last_prices")

def extract_price(soup):
    selectors = [
        "span.a-price .a-offscreen",
        "span#priceblock_ourprice",
        "span#priceblock_dealprice",
        "span#apex_price_string",
        "span#tp_price_block_total_price_ww",
        "span.a-price-whole",
    ]
    for sel in selectors:
        elem = soup.select_one(sel)
        if elem:
            price = elem.text.strip()

            if "%" in price:
                continue

            price = price.replace("₹", "").replace("â‚¹", "").replace(",", "").strip()

            if price.replace(".", "", 1).isdigit():
                return price
    return None

def track_product(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_elem = soup.select_one("h1 span, span#productTitle")
    title = title_elem.text.strip() if title_elem else "Unknown Product"

    price = extract_price(soup)

    print(f"\n🔍 Checking: {title}")
    print(f"💰 Price: {price}")

    # Unique file per product
    asin = url.split("/")[-2]
    last_file = f"last_prices/{asin}.txt"

    # Load previous price
    last_price = None
    if os.path.exists(last_file):
        with open(last_file, "r") as f:
            last_price = f.read().strip()

    # Save CSV
    with open("amazon_prices.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            title,
            price
        ])

    # Compare and send email
    if last_price and price and (last_price != price):
        send_email(
            subject=f"⚠️ Price Change: {title}",
            message=f"Old Price: ₹{last_price}\nNew Price: ₹{price}\nURL: {url}"
        )

    # Update last price
    with open(last_file, "w") as f:
        f.write(price if price else "")


print(f"📦 Tracking {len(urls)} products...")

for u in urls:
    track_product(u)

print("\n✅ Done.")
