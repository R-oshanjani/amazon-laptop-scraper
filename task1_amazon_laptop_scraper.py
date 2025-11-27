import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.amazon.in/s"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def fetch_page(page_num):
    params = {"k": "laptop", "page": page_num}
    for attempt in range(3):
        try:
            r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
            print(f"Page {page_num} attempt {attempt+1} status:", r.status_code)
            if r.status_code == 200:
                return r.text
            time.sleep(3)
        except Exception as e:
            print("Error while requesting page", page_num, ":", e)
            time.sleep(3)
    return None


def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
    products = []

    for b in blocks:
        title_tag = b.h2
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)

        img_tag = b.find("img", class_="s-image")
        image = img_tag["src"] if img_tag else None

        rating_tag = b.find("span", class_="a-icon-alt")
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        price_tag = b.find("span", class_="a-price-whole")
        price = price_tag.get_text(strip=True) if price_tag else None

        sponsor = b.find("span", string=lambda s: s and "Sponsored" in s)
        result_type = "Ad" if sponsor else "Organic"

        products.append(
            {
                "Image": image,
                "Title": title,
                "Rating": rating,
                "Price": price,
                "Result_Type": result_type,
            }
        )

    return products


def main():
    all_products = []

    for page in range(1, 4):
        print("\nScraping page", page)
        html = fetch_page(page)
        if not html:
            print("Failed to get HTML for page", page)
            continue

        page_products = parse_products(html)
        print("Products found on page", page, ":", len(page_products))
        all_products.extend(page_products)
        time.sleep(2)

    if not all_products:
        print("NO PRODUCTS SCRAPED. Most likely Amazon blocked this IP (503 / Oops page).")
        return

    df = pd.DataFrame(all_products)
    filename = f"amazon_laptops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print("Saved:", filename)


if __name__ == "__main__":
    main()
