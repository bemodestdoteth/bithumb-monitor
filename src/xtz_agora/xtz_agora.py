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
from config import prior_setup_selenium
import json

@prior_setup_selenium
def xtz_agora_scrape(coin, driver, delay):
    # Storing post
    base_url = "https://www.tezosagora.org/"

    # Open proposal combobox
    driver.find_element(by=By.CSS_SELECTOR, value='div._agoraSelect_95594').click()
    WebDriverWait(driver, delay).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div._agoraSelect__menu__item_95594')))

    # Topmost Proposal
    current_proposal = driver.find_element(by=By.CSS_SELECTOR, value='div._agoraSelect__menu__item_95594').text
    latest_proposal = {
        'title' : current_proposal,
        'link': "{}period/{}".format(base_url, current_proposal[:2])
    }
    
    driver.quit()

    # First time scraping
    if coin["post"] == "":
        update_post(latest_proposal, coin['name'])
        return "New"
    elif json.loads(coin["post"]) == latest_proposal:
        return None
    else:
        update_post(latest_proposal, coin['name'])
        # Return post to send telegram message
        latest_proposal['name'] = coin['name']
        return latest_proposal

# Testing code
if __name__ == "__main__":
    xtz_agora_scrape(get_coin("XTZ"))