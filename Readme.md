<h1 align="center">PULSE-WEBSCRAPING</h1>

<p align="center"><em>Uncover Insights, Drive Innovation, Transform Collaboration</em></p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/niteshjangid29/pulse-webscraping?style=flat&logo=git&logoColor=white&color=0080ff" />
  <img src="https://img.shields.io/github/languages/top/niteshjangid29/pulse-webscraping?style=flat&color=0080ff" />
  <img src="https://img.shields.io/github/languages/count/niteshjangid29/pulse-webscraping?style=flat&color=0080ff" />
</p>

<p align="center"><em>Built with the tools and technologies:</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" />
  <img src="https://img.shields.io/badge/Selenium-43B02A.svg?style=flat&logo=Selenium&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" />
</p>

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Getting Started](#%EF%B8%8F-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
- [Arguments](#-arguments)
- [Sample JSON Output](#-sample-json-output)

---

## 🔍 Overview

**pulse-webscraping** automates the extraction of product reviews from **G2**, enabling efficient data collection and structured analysis.  
It uses **Selenium** + **BeautifulSoup** to navigate G2’s review pages, parse review data, and store it in JSON.  
The scraper supports **date filtering** and outputs reviews with structured reviewer details and review text.

---

## ✨ Features

- 🧩 **Review Extraction:** Collects reviews within a specified date range.  
- 🧭 **Browser Automation:** Navigates G2 product review pages automatically.  
- 📊 **Structured Data:** Extracts rating, reviewer info, badges, pros, cons, problems solved, and review URL.  
- ⚙️ **Error Handling:** Handles retries and skips invalid reviews.  
- 💾 **JSON Output:** Saves reviews in clean JSON for downstream analysis.  

---

## ⚙️ Getting Started

### Prerequisites
- **Python:** 3.8+  
- **pip:** Python package manager  
- **Google Chrome + ChromeDriver** (matching versions)  

### Installation

1. Clone repository  
```sh
git clone https://github.com/niteshjangid29/pulse-webscraping
```

2. **Navigate to the project directory**
```sh
cd pulse-webscraping
```

3. **Install dependencies**
```sh
pip install -r requirements.txt
```

## 🚀 Usage

Run the project with:
```sh
python3 g2_scraper.py -c <COMPANY_NAME> -s <START_DATE> -e <END_DATE> -o <OUTPUT_FILE>
```

## ⚙️ Arguments
- `-c / --company` — company/product to search on G2 (required)

- `-s / --start_date` — start date (YYYY-MM-DD) (required)

- `-e / --end_date` — end date (YYYY-MM-DD). If omitted, defaults to `today`.

- `-o / --output` — output filename (default: `g2_reviews.json`)

**Examples:**

- Minimal (start date + company). End date defaults to today:
```sh
python3 g2_scraper.py -c Slack -s 2025-09-03
```

- Full range and explicit output file:
```sh
python3 g2_scraper.py -c Slack -s 2025-09-03 -e 2025-09-13 -o slack_reviews.json
```

- Long-form flags (identical behaviour):
```sh
python3 g2_scraper.py --company "Slack" --start_date 2025-09-03 --end_date 2025-09-13 --output slack_reviews.json
```


## Sample Output JSON

```sh
[
  {
    "rating": 4.5,
    "date": "2025-09-10",
    "url": "https://www.g2.com/products/slack/reviews/slack-review-11665819",
    "reviewer": {
      "name": "Satyanjani S.",
      "role": "Projet Manager",
      "company_size": "Enterprise (> 1000 emp.)",
      "badges": [
        "Current User",
        "Validated Reviewer",
        "Source: Organic"
      ]
    },
    "review_text": {
      "title": "\"Best-in-Class for Team Chat and Seamless Collaboration\"",
      "pros": "Slack makes team communication effortless with its clean interface, powerful search, and seamless integrations with tools we use daily. I especially like how channels keep conversations organized and reduce email clutter, making collaboration faster and more transparent Review collected by and hosted on G2.com.",
      "cons": "At times, Slack can feel overwhelming with constant notifications, especially in large teams with many active channels. It takes some discipline and customization to manage alerts and avoid distractions. Also, the pricing can be on the higher side compared to alternatives if you need the premium features Review collected by and hosted on G2.com.",
      "problems_solved": "Slack centralizes all our team communication in one place, reducing reliance on long email chains and scattered chats. With channels, we can keep conversations topic-focused, which saves time and improves transparency. Integrations with tools like Google Drive and Jira streamline workflows, so we can share updates instantly and act faster. Overall, it makes collaboration more efficient and keeps everyone aligned, especially in a hybrid work environment Review collected by and hosted on G2.com."
    }
  },
  {
    "rating": 4.5,
    "date": "2025-09-10",
    "url": "https://www.g2.com/products/slack/reviews/slack-review-11662901",
    "reviewer": {
      "name": "Arjun G.",
      "role": "Associate Salesforce Consultant",
      "company_size": "Small-Business (50 or fewer emp.)",
      "badges": [
        "Current User",
        "Validated Reviewer",
        "Source: Organic"
      ]
    },
    "review_text": {
      "title": "\"Always ahead in the conversation with Slack Summary\"",
      "pros": "The best part about using Slack with so many clients and team members is that you can summarize what they want to convey and had a conversation around in the channels. Without looking at the long conversation, a quick glance and they call to action are provided seamlessly.",
      "cons": "The documentation for the slack features are not well prepared, that is the only downside of the slack. I had conversation with their customer support about it and they communicated that they will fix it as we wanted to implement salesforce with slack. Review collected by and hosted on G2.com.",
      "problems_solved": "Slack solves the major problem of finding the right resource in the least time and reducing the messaging workload with its AI features. Review collected by and hosted on G2.com."
    }
  },
]
```