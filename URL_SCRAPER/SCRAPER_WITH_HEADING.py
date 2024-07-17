import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import urllib.request
from urllib.parse import urlparse, urljoin
import random
import os

# Custom headers for the browser
custom_headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    'User-Agent': "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36",
}

# Set up the browser
service = Service(executable_path=r"C:\Users\Soumil\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Toggle this for 403 errors
options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
options.add_argument('custom_headers')
driver = webdriver.Chrome(service=service, options=options)

def extract_data(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').text
    paragraphs = [p.text for p in soup.find_all('p')]
    
    data_tables = soup.find_all('table')
    table_data = ''
    for i, table in enumerate(data_tables):
        table_data += f"Table {i+1}:\n"
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            row_data = [col.text.strip() for col in cols]
            table_data += ', '.join(row_data) + '\n'
        table_data += '\n'

    output = ''
    output += f'Title: {title}\n'
    for paragraph in paragraphs:
        output += f'Text: {paragraph}\n'
    output += table_data
    output += '\n'
    return title, output

def wait_if_required():
    if random.random() < 0.1:  # 10% chance of waiting
        time.sleep(10)
        print("Waiting for 10 seconds...")

def process_urls(url_list):
    with open('Heading.txt', 'w', encoding='utf-8') as heading_file, open('Content.txt', 'w', encoding='utf-8') as content_file:
        for i, url in enumerate(url_list, start=1):
            if not url.startswith('http'):
                print(f"Invalid URL: {url}")
                continue
            try:
                wait_if_required()
                title, data = extract_data(url)
                heading_file.write(f"Link: {url}\nHeading: {title}\n\n")
                content_file.write(f"Source {i}: {url}\n{data}\n")
            except Exception as e:
                print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    urls = [
        ##MONO ETHELENE GYCOL LINKS:
        "https://www.coherentmarketinsights.com/market-insight/monoethylene-glycol-market-4930#:~:text=Monoethylene%20glycol%20is%20used%20in,%2C%20medicines%2C%20and%20chemical%20processing.",
        "https://www.researchandmarkets.com/reports/5462902/2024-mono-ethylene-glycol-meg-market-outlook",
        "https://www.marketreportsworld.com/enquiry/request-sample/24471125?utm_source=lilyLinkden&trk=article-ssr-frontend-pulse_little-text-block", ## paid
        "https://www.researchandmarkets.com/reports/3150623/monoethylene-glycol-meg-2024-world-market",
        "https://mcgroup.co.uk/researches/monoethylene-glycol-meg",
        "https://www.chemanalyst.com/industry-report/india-ethylene-oxide-market-28",
        "https://www.chemanalyst.com/industry-report/mono-ethylene-glycol-meg-market-646",
        "https://www.chemanalyst.com/NewsAndDeals/NewsDetails/global-meg-prices-fall-entering-april-2024-high-inventories-to-blame-27391",
        "https://www.chemanalyst.com/NewsAndDeals/NewsDetails/supply-issues-lead-to-low-coastal-inventory-driving-us-meg-prices-higher-28943",
        "https://www.chemanalyst.com/NewsAndDeals/NewsDetails/meg-prices-drop-in-late-may-2024-in-north-america-amid-high-inventory-and-supply-28263",
        "https://www.chemanalyst.com/NewsAndDeals/NewsDetails/technip-energies-acquires-shells-cutting-edge-technology-for-boosting-bio-polyester-28660",
    ]
    process_urls(urls)
