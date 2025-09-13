import argparse
from datetime import datetime, date
import time
import json
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

# Parse individual review card
def parse_review_card(card):
    # Rating
    rating_meta = card.find("meta", attrs={"itemprop": "ratingValue"})
    rating = float(rating_meta["content"]) if rating_meta else None

    # Reviewer
    reviewer_meta = card.find("meta", attrs={"itemprop": "name"})
    reviewer = reviewer_meta["content"] if reviewer_meta else ""

    # Reviewer details (title, company size)
    reviewer_details = []
    details_blocks = card.select("div.elv-tracking-normal.elv-text-xs")
    for block in details_blocks:
        reviewer_details.append(block.get_text(strip=True))

    # Date
    date_meta = card.find("meta", attrs={"itemprop": "datePublished"})
    review_date = date_meta["content"] if date_meta else ""

    # Title
    title_div = card.find("div", attrs={"itemprop": "name"})
    title = title_div.get_text(strip=True) if title_div else ""

    # Review Body
    body_div = card.find("div", attrs={"itemprop": "reviewBody"})
    review_parts = []
    if body_div:
        review_parts.extend(p.get_text(" ", strip=True) for p in body_div.find_all("p"))
    
    # Pros
    pros_block = card.find("span", string=lambda s: s and "Pros" in s)
    if pros_block:
        pros_p = pros_block.find_next("p")
        if pros_p:
            review_parts.append(f"Pros: {pros_p.get_text(' ', strip=True)}")

    # Cons
    cons_block = card.find("span", string=lambda s: s and "Cons" in s)
    if cons_block:
        cons_p = cons_block.find_next("p")
        if cons_p:
            review_parts.append(f"Cons: {cons_p.get_text(' ', strip=True)}")
    
    review = " ".join(review_parts).strip()

    # Review URL
    url_btn = card.find("button", attrs={"data-clipboard-text": True})
    review_url = url_btn["data-clipboard-text"] if url_btn else ""

    return {
        "rating": rating,
        "reviewer": reviewer,
        "reviewer_details": reviewer_details,
        "date": review_date,
        "title": title,
        "review": review,
        "url": review_url,
    }
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
