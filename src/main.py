import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import re
import random
import os
from dotenv import load_dotenv

load_dotenv()


# Configuration
CHROME_DRIVER = os.getenv("CHROME_DRIVER")
BASE_DOMAIN = os.getenv("BASE_DOMAIN")
BASE_URL = "https://{BASE_DOMAIN}/#/companies?qOrganizationName=payment%20gateway&organizationLocations[]=Americas&organizationLocations[]=United%20States&organizationLocations[]=Europe&organizationLocations[]=Germany&organizationLocations[]=France&organizationLocations[]=Canada&organizationLocations[]=United%20Kingdom&page=1&sortAscending=false&sortByField=recommendations_score"
NUM_PAGES = int(os.getenv("NUM_PAGES", 2))                                  # scrape 2 pages
OUTPUT_FILE = "../data/payment_gateways.csv"


# Mapping country string to a broad region bucket
REGION_MAP = {
    "united kingdom": "UK",
    "england":        "UK",
    "scotland":       "UK",
    "wales":          "UK",
    "ireland":        "Europe",
    "france":         "Europe",
    "germany":        "Europe",
    "spain":          "Europe",
    "italy":          "Europe",
    "netherlands":    "Europe",
    "sweden":         "Europe",
    "norway":         "Europe",
    "finland":        "Europe",
    "portugal":       "Europe",
    "switzerland":    "Europe",
    "romania":        "Europe",
    "bulgaria":       "Europe",
    "cyprus":         "Europe",
    "poland":         "Europe",
    "czechia":        "Europe",
    "lithuania":      "Europe",
    "united states":  "Americas",
    "us":             "Americas",
    "canada":         "Americas",
    "brazil":         "Americas",
    "mexico":         "Americas",
    "argentina":      "Americas",
    "delaware":       "Americas",
    "nevada":         "Americas",
    "california":     "Americas",
    "new york":       "Americas",
    "massachusetts":  "Americas",
    "florida":        "Americas",
    "michigan":       "Americas",
    "washington":     "Americas",
    "arizona":        "Americas",
}

def bucket_region(location: str) -> str:
    loc_lower = location.lower()
    for key, region in REGION_MAP.items():
        if key in loc_lower:
            return region
    return "Other"


# Selenium setup
options = uc.ChromeOptions()
options.add_argument(f"user-data-dir={os.getenv('CHROME_USER_DATA_DIR')}")
options.add_argument(f"profile-directory={os.getenv('CHROME_PROFILE_DIRECTORY')}")
driver = uc.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 60)


# CSV setup
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "website", "location", "region", "employee_size", "industries", "keywords"])


    # Main loop over pages
    for page in range(1, NUM_PAGES + 1):
        url = BASE_URL + str(page)
        print(f"\n→ Page {page}: {url}")
        driver.get(url)

        # Manual CAPTCHA for first page
        if page == 1:
            input("Please complete the CAPTCHA manually and press [Enter] to continue...")

        # Wait until at least one company row is rendered
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-shell-view='non-groupby-table']//div[@role='row' and @aria-rowindex='0']")
            )
        )
        
        time.sleep(random.randint(4, 8))  

        def first_text(el, xpath):
            try:
                return el.find_element(By.XPATH, xpath).text.strip()
            except:
                return ""

        rows = driver.find_elements(By.XPATH, "//div[@data-shell-view='non-groupby-table']//div[@role='row' and starts-with(@id,'table-row-')]")
        print(f"   • Found {len(rows)} companies on this page")

        for row in rows:
            name          = first_text(row, ".//div[@aria-colindex='1']//a/span")
 
            # Website icon is the first link with aria-label containing 'website'
            try:
                website_el = row.find_element(By.XPATH, ".//a[contains(@aria-label,'website')]")
                website = website_el.get_attribute("href")
            except:
                website = ""

            employee_size = first_text(row, ".//div[@aria-colindex='4']//span[@data-count-size]")
            industries    = first_text(row, ".//div[@aria-colindex='6']//span[@class='zp_z4aAi']")
            location      = first_text(row, ".//div[@aria-colindex='8']//span[contains(@class,'zp_FEm_X')]")
            region        = bucket_region(location) if location else ""

            keyword_els = row.find_elements( By.XPATH, ".//div[@aria-colindex='7']//span[not(starts-with(text(), '+'))]")
            keywords = [el.text.strip() for el in keyword_els][:2]   # first ≤2 pills
            keywords_str = "; ".join(keywords) 

            writer.writerow([name, website, location, region, employee_size, industries, keywords_str])

            # Short log line to watch progress in real time
            print(f"     - {name:40.40s} | {region:8s} | {employee_size:>5s}")

            # exit here for test
        

print(f"\n Done!  Results saved to {OUTPUT_FILE}")

driver.quit()