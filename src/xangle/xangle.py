from selenium.webdriver.common.by import By

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
def xangle_scrape(coin, driver, delay):
    # Topmost Proposal
    latest_proposal = {
        'title' : driver.find_element(by=By.CSS_SELECTOR, value='p.title.mt8').text,
        'link': driver.find_element(by=By.CSS_SELECTOR, value='.bc-insight-list-item-wrapper').get_attribute('href')
    }

    driver.quit()
    
    # First time scraping
    if coin["post"] == "":
        update_post(latest_proposal, coin['name'])
        return "New"
    elif json.loads(coin["post"]) == latest_proposal:
        return None
    else:
        # Return post to send telegram message
        update_post(latest_proposal, coin['name'])
        latest_proposal['name'] = coin['name']
        return latest_proposal

# Testing code
if __name__ == "__main__":
    xangle_scrape(get_coin("ETC"))