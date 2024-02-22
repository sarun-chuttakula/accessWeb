import csv
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def update_csv():
    # Function to check website content and status code
    def check_website(row):
        uuid, status_code, urls = row
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Initialize updated_status as success
        updated_status = status_code

        for url in urls.split(','):
            try:
                driver.get(url.strip())
                current_status = driver.execute_script("""
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", window.location.href, false);
                    xhr.send(null);
                    return xhr.status;
                """)

                # If any URL's status is not 200 or 201, update updated_status
                if current_status not in [200, 201]:
                    updated_status = current_status
                    break
            except Exception as e:
                logging.error(f"Error occurred while processing URL: {url.strip()}. Error: {e}")

        # Close the driver
        driver.quit()

        return [uuid, status_code, urls, updated_status]

    # Read URLs from CSV file
    csv_file = '/home/xelpmoc/Documents/Code/accessweb/data/jobs.csv'
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Get header
            rows = list(reader)
    except Exception as e:
        logging.error(f"Error occurred while reading CSV file: {csv_file}. Error: {e}")
        return

    # List to store updated rows
    updated_rows = []

    # Iterate over each row and update
    try:
        for row in rows:
            updated_rows.append(check_website(row))
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")

    # Append the updated_status_code column to the header
    header.append('updated_status_code')

    # Write updated data back to the CSV file
    try:
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write updated header
            writer.writerows(updated_rows)  # Write updated rows
        logging.info("CSV file updated successfully.")
    except Exception as e:
        logging.error(f"Error occurred while writing to CSV file: {csv_file}. Error: {e}")

# Call the function to update the CSV
update_csv()
