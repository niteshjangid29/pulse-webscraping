import argparse
from datetime import datetime, date
import time
import json
import re
from dateutil import parser as date_parser

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Parse CLI arguments
def parse_args():
    today = date.today().isoformat()
    p = argparse.ArgumentParser(description="G2 Scraper")
    p.add_argument("--company", "-c", required=True, help="Company name e.g. 'Slack'")
    p.add_argument("--start_date", "-s", required=True, help="Start date (YYYY-MM-DD)")
    p.add_argument("--end_date", "-e", default=today, help="End date (YYYY-MM-DD)")
    p.add_argument("--output", "-o", help="Output JSON filename")
    return p.parse_args()

# Setup Driver
def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def parse_review_card(card):
    """Parse a single G2 review card <article> into structured JSON."""

    review = {}

    # --- Rating ---
    rating_tag = card.find("meta", itemprop="ratingValue")
    review["rating"] = float(rating_tag["content"]) if rating_tag else None

    # --- Date ---
    date_tag = card.find("meta", itemprop="datePublished")
    review["date"] = date_tag["content"] if date_tag else None

    # --- Review URL ---
    url_btn = card.find("button", attrs={"data-clipboard-text": True})
    review["url"] = url_btn["data-clipboard-text"] if url_btn else None

    # --- Reviewer info ---
    reviewer = {}
    name_tag = card.select_one('[itemprop="author"] meta[itemprop="name"]')
    reviewer["name"] = name_tag["content"].strip() if name_tag else None

    # Role + Company size (subtle text blocks)
    subtle_tags = card.select("div.elv-text-subtle")
    if subtle_tags:
        reviewer["role"] = subtle_tags[0].get_text(strip=True)
    if len(subtle_tags) > 1:
        reviewer["company_size"] = subtle_tags[1].get_text(strip=True)

    # Badges (exclude "Rating Updated ..." or anything resembling a date)
    badges = []
    for badge in card.select("label.elv-font-medium"):
        txt = badge.get_text(strip=True)
        if re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", txt):  # matches mm/dd/yyyy or dd/mm/yyyy
            continue
        if txt and not txt.lower().startswith("rating updated"):
            badges.append(txt)
    reviewer["badges"] = badges

    review["reviewer"] = reviewer

    # --- Review text sections ---
    review_text = {}

    # Title
    title_tag = card.find("div", itemprop="name")
    if title_tag:
        inner = title_tag.find("div")
        review_text["title"] = inner.get_text(strip=True) if inner else None

    # Pros
    pros_heading = card.find("div", string=lambda t: t and "like best" in t.lower())
    if pros_heading:
        p = pros_heading.find_next("p")
        review_text["pros"] = p.get_text(" ", strip=True) if p else None

    # Cons
    cons_heading = card.find("div", string=lambda t: t and "dislike" in t.lower())
    if cons_heading:
        p = cons_heading.find_next("p")
        review_text["cons"] = p.get_text(" ", strip=True) if p else None

    # Problems solved
    problems_heading = card.find("div", string=lambda t: t and "problems" in t.lower())
    if problems_heading:
        p = problems_heading.find_next("p")
        review_text["problems_solved"] = p.get_text(" ", strip=True) if p else None

    review["review_text"] = review_text

    return review

# Main Scraping Logic
def g2_scraper(company, start_date, end_date, output_file):
    driver = setup_driver()
    wait = WebDriverWait(driver, 5)

    try:
        print("Navigating to G2...")
        driver.get("https://www.g2.com/")
        
        search_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='query']"))
        )
        driver.execute_script("arguments[0].focus();", search_input)
        search_input.clear()
        print(f"Searching for company: {company}")
        search_input.send_keys(company)
        search_input.send_keys(Keys.RETURN)

        # Retry logic for loading the company page
        for _ in range(3):
            try:
                company_link = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/products/'][href*='/reviews']"))
                )
                driver.execute_script("arguments[0].click();", company_link)
                print("Navigating to company reviews page...")
                break
            except Exception as e:
                print(f"Error occurred while navigating: {e}")
                time.sleep(1)

        # Wait for the reviews page to load
        time.sleep(3)

        reviews = []
        stop_scraping = False

        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract reviews
            cards = soup.select("div[data-poison] article")
            for card in cards:
                parsed = parse_review_card(card)

                review_date = None
                if parsed["date"]:
                    try:
                        review_date = date_parser.parse(parsed["date"]).date()
                        parsed["date"] = review_date.isoformat()
                    except ValueError:
                        parsed["date"] = None

                # Filter by date range
                # if review_date:
                #     if review_date < start_date:
                #         print("Reached reviews older than start date. Stopping scraping.")
                #         stop_scraping = True
                #         break  # stop processing current page
                #     if review_date > end_date:
                #         continue  # skip too-new review

                if review_date:
                    if not (start_date <= review_date <= end_date):
                        continue  # skip reviews outside date range

                reviews.append(parsed)
                print(f"Collected review by {parsed['reviewer']} on {parsed['date']}")

            if stop_scraping:
                break

            # --- Look for Next Page link
            next_link = soup.find("a", string=lambda s: s and "Next" in s)
            if not next_link:
                next_link = soup.select_one("a.pagination__named-link[href*='page=']")

            if next_link and next_link.get("href"):
                next_url = next_link["href"]
                if not next_url.startswith("http"):
                    next_url = "https://www.g2.com" + next_url
                print(f"➡️ Navigating to next page: {next_url}")
                print(f"   Total reviews collected so far: {len(reviews)}")
                driver.get(next_url)
                time.sleep(3)
            else:
                print("No more pages found. Stopping.")
                break
        
        if not output_file:
            output_file = f"g2_reviews_{company.lower().replace(' ', '_')}.json"
        # Save reviews in JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Collected {len(reviews)} reviews. Saved to {output_file}")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    args = parse_args()
    start_date = datetime.fromisoformat(args.start_date).date()
    end_date = datetime.fromisoformat(args.end_date).date()
    g2_scraper(args.company, start_date, end_date, args.output)
