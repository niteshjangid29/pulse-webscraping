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

**pulse-webscraping** is a robust developer tool that automates the extraction of company reviews from **G2**, enabling efficient data collection and analysis.  
It leverages **web scraping** and **browser automation** to navigate, parse, and store review data in a structured JSON format — supporting insights into customer sentiment and feedback trends.

---

## ✨ Features

- 🧩 **Review Extraction:** Automates the collection of reviews within specified date ranges for comprehensive analysis.  
- 🧭 **Browser Automation:** Navigates complex G2 web pages seamlessly to ensure accurate data scraping.  
- 📊 **Structured Data Output:** Saves reviews in JSON format, facilitating easy integration with analysis tools.  
- ⚙️ **Environment Management:** Ensures consistent setup with dependency management for reliable execution.  
- 💬 **Sentiment & Trend Analysis:** Supports insights into customer feedback and product reputation.  

---

## ⚙️ Getting Started

### Prerequisites
This project requires the following:
- **Programming Language:** Python 3.8+  
- **Package Manager:** pip  
- **Browser Driver:** Google Chrome + ChromeDriver  

### Installation

1. **Clone the repository**
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

🚀 **Usage**

Run the project with:
```sh
python3 g2_scraper.py -c <COMPANY_NAME> -s <START_DATE> -e <END_DATE> -o <OUTPUT_FILE>
```

**Example:**
```sh
python3 g2_scraper.py -c Slack -s 2025-01-01 -e 2025-09-13 -o slack_reviews.json
```