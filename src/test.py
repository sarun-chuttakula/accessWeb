from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading

# Function to check website content
def check_website_content(url):
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    print(f"Title of {url}: {driver.title}")
    # You can add your content checking logic here

    driver.quit()

# List of websites
websites = ["https://python.org", "https://www.wikipedia.org", "https://www.bbc.com", "https://www.reddit.com", "https://www.google.com","https://dejobs.org/san-antonio-tx/administrative-assistant-fuels-regulatory-compliance/3CB4D6E9C345476DA87D3F9F7D519E4E/job/"]

# Create threads for each website
threads = []
for url in websites:
    thread = threading.Thread(target=check_website_content, args=(url,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
