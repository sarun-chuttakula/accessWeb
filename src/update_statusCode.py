import csv
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to check website content and status code
def check_website(row, results):
    uuid, status_code, urls = row
    options = Options()
    options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Initialize updated_status as success
    updated_status = status_code

    for url in urls.split(','):
        retry_count = 5
        while retry_count > 0:
            driver.get(url.strip())
            current_status = driver.execute_script("""
                var xhr = new XMLHttpRequest();
                xhr.open("GET", window.location.href, false);
                xhr.send(null);
                return xhr.status;
            """)
            # If any URL's status is not 200 or 201, update updated_status
            if current_status in [200, 201]:
                break
            else:
                retry_count -= 1
                time.sleep(1)  # Wait for 1 second before retrying

        if retry_count == 0:  # If all retries failed
            updated_status = "Failed"
            # Write the failed URL to a separate CSV file
            with open('failed.csv', 'a', newline='') as failed_file:
                failed_writer = csv.writer(failed_file)
                failed_writer.writerow([uuid, url.strip()])

    # Append result to results list
    results.append([uuid, status_code, urls, updated_status])

    # Close the driver
    driver.quit()

# Read URLs from CSV file
csv_file = '/home/xelpmoc/Documents/Codes/accessWeb/data/jobs.csv'
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Get header
    rows = list(reader)

# List to store results
results = []

# List to store threads
threads = []

# Start a thread for each row
for row in rows:
    thread = threading.Thread(target=check_website, args=(row, results))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Write updated data back to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header + ['updated_status_code'])  # Write updated header
    writer.writerows(results)  # Write updated rows
