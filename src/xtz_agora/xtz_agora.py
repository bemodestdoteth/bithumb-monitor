from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Import file from parent directory
from pathlib import Path
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_coin, update_post
from config import prior_setup_selenium, print_n_log
import json

@prior_setup_selenium
def mintscan_scrape(coin, driver, delay = 5):
    # Storing post
    base_url = "https://www.tezosagora.org/"
    latest_number = int(coin["link"].split("/")[-1])

    # First time scraping: store latest proposal
    if coin["post"] == "":
        # Open website
        driver.get(coin["link"])
        WebDriverWait(driver, delay).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div._header__logo_dfbb2')))
        latest_proposal = {
            'title' : "XTZ Proposal #{}".format(latest_number),
            'link': coin['link']
        }

        update_post(latest_proposal, coin['name'])
        return None
    else:
        new_url = coin['link'][:-2] + str(latest_number + 1)
        driver.get(new_url)
        WebDriverWait(driver, delay).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div._header__logo_dfbb2')))

        if driver.find_element(by=By.CSS_SELECTOR, value='.div._noProposals_e5a94') is None:
            return None
        else:
            update_post(latest_proposal, coin['name'])

        # Return post to send telegram message
        latest_proposal['name'] = coin['name']
        return latest_proposal

# Testing code
mintscan_scrape(get_coin("XTZ"))