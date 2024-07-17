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
    return output

def wait_if_required():
    if random.random() < 0.1:  # 10% chance of waiting
        time.sleep(10)
        print("Waiting for 10 seconds...")

def process_urls(url_list):
    with open('Scraper_test.txt', 'w', encoding='utf-8') as file:
        for i, link in enumerate(url_list, start=1):
            wait_if_required()
            file.write(f"Source {i}: {link}\n")
            data = extract_data(link)
            file.write(data + '\n')


if __name__ == "__main__":
    urls = [
        "https://www.screener.in/company/RELIANCE/consolidated/"
    ]
    process_urls(urls)
