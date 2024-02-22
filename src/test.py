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

    status_code_script = """
    var xhr = new XMLHttpRequest();
    xhr.open("GET", window.location.href, false);
    xhr.send(null);
    return xhr.status;
    """
    status_code = driver.execute_script(status_code_script)
    print(f"Status code of {url}: {status_code}")
    driver.quit()

# List of websites
websites = ["https://dejobs.org/mumbai-ind/senior-rd-associate-cti/9686A3A1326340C6A6DEAF42E7DD6ADE/job/"]

# Create threads for each website
threads = []
for url in websites:
    thread = threading.Thread(target=check_website_content, args=(url,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
