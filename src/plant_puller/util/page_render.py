from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

from markdownify import MarkdownConverter

def scrape_webpage(url):
    # Try with requests first (for HTML content)
    page_source=""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Set the page source for cleaning
            return clean_page(response.content)

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
        return clean_page(page_source)

    except Exception as e:
        print(f"Selenium failed: {e}")
        return None


def clean_page(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    soup = soup.find('body')

    for item in soup.find_all('style'):
        item.decompose()
    
    for item in soup.find_all('script'):
        item.decompose()

    return MarkdownConverter().convert_soup(soup)


if __name__=="__main__":
  # Example Usage
  url = "https://www.goodhousekeeping.com/home/gardening/g40742429/best-indoor-plants-for-health/"
  content = scrape_webpage(url)
  with open("tmp.txt", "+w") as f:
    f.write(content)
  #with open("tmp2.txt", "+w") as f:
  #  f.write(html2markdown.convert(content))