from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

import html2markdown

def scrape_webpage(url):
    # Try with requests first (for HTML content)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content.text
            #soup = BeautifulSoup(response.content, 'html.parser')
            
            #body_content = soup.body  # Extract content from <body> tag
            #if body_content:
            #    return body_content.prettify()
    except Exception as e:
        print(f"Requests failed: {e}")

    # If requests fail or JavaScript rendering is needed, use selenium
    try:
        # Configure selenium to run headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        # Set up WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        
        # Wait for JavaScript to render (adjust time as needed)
        time.sleep(5)  # Increase or decrease based on your needs
        
        # Extract page source and close the browser
        page_source = driver.page_source
        driver.quit()
        
        # Use BeautifulSoup to parse and target the <body> content
        #soup = BeautifulSoup(page_source, 'html.parser')
        return page_source
        #body_content = soup.body  # Extract content from <body> tag
        #if body_content:
        #    return body_content.prettify()
    except Exception as e:
        print(f"Selenium failed: {e}")
        return None


if __name__=="__main__":
  # Example Usage
  url = "https://www.goodhousekeeping.com/home/gardening/g40742429/best-indoor-plants-for-health/"
  content = scrape_webpage(url)
  print(content)
  with open("tmp.txt", "+w") as f:
    f.write(content)
  with open("tmp2.txt", "+w") as f:
    f.write(html2markdown.convert(content))