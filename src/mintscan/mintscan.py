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
def mintscan_scrape(coin, driver, delay):
    # Topmost Proposal
    latest_proposal = {
        'title' : driver.find_element(by=By.CSS_SELECTOR, value='div h2').text,
        'link': driver.find_element(by=By.CSS_SELECTOR, value='div.ProposalCard_rightArrowWrapper__3lX_p a.ProposalCard_link__38deC').get_attribute('href')
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
#mintscan_scrape(get_coin("ATOLO"))