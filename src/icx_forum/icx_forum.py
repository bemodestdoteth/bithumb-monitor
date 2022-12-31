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
def icx_forum_scrape(coin, driver, delay = 5):
    # Topmost Proposal
    latest_proposal = {
        'title' : driver.find_element(by=By.CSS_SELECTOR, value='span.topic-title').text,
        'link': driver.find_element(by=By.CSS_SELECTOR, value='a.search-link').get_attribute('href')
    }

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
#icx_forum_scrape(get_coin("ICX"))