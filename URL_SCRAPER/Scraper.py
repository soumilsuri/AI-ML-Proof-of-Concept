'''
Selenium scraper - Scrapes internal links(no images)
for images use: images = [img.get('src') for img in soup.find_all('img')] 
    for image in images:
        output += f'Image: {image}\n'
this code is commented below
'''
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import random
import time
import urllib.request
from urllib.parse import urlparse, urljoin
import csv
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
#link to download chrome driver: https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/win64/chromedriver-win64.zip
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Toggle this for 403 errors
options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
options.add_argument('custom_headers')
driver = webdriver.Chrome(service=service, options=options)

def extract_internal_links(url):
    internal_links = []
    external_links = []
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        a_tags = driver.find_elements(By.TAG_NAME, "a")
        for tag in a_tags:
            href = tag.get_attribute("href")
            if href:
                parsed_href = urlparse(href)
                if not parsed_href.netloc or parsed_href.netloc == urlparse(url).netloc or parsed_href.netloc.startswith('https'):
                    ilink = urljoin(url, href)
                    if ilink.startswith('http'):
                        internal_links.append(ilink)
                    else:
                        external_links.append(href)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return internal_links

def extract_data(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').text
    paragraphs = [p.text for p in soup.find_all('p')]
    # images = [img.get('src') for img in soup.find_all('img')]
    
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
    # for image in images:
    #     output += f'Image: {image}\n'
    output += table_data
    output += '\n'
    return output

def wait_if_required():
    if random.random() < 0.1:  # 10% chance of waiting
        time.sleep(10)
        print("Waiting for 10 seconds...")

def process_urls(url_list):
    all_links = []
    for url in url_list:
        if not url.startswith('http'):
            print(f"Invalid URL: {url}")
            continue
        try:
            internal_links = extract_internal_links(url)
            all_links.extend(internal_links)
        except Exception as e:
            print(f"Error: {e}")

    with open('Scraper_test.txt', 'w', encoding='utf-8') as file:
        for i, link in enumerate(all_links, start=1):
            wait_if_required()
            file.write(f"Source {i}: {link}\n")
            data = extract_data(link)
            file.write(data + '\n')


if __name__ == "__main__":
    urls = [
    "https://www.coherentmarketinsights.com/market-insight/monoethylene-glycol-market-4930#:~:text=Monoethylene%20glycol%20is%20used%20in,%2C%20medicines%2C%20and%20chemical%20processing."
    ]
    process_urls(urls)
