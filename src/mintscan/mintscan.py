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
from dotenv import load_dotenv
import json
import logging

# Adding system path for import

# Environment Variables
load_dotenv()

@prior_setup_selenium
def mintscan_scrape(coin, driver, delay = 5):
    try:
        # Logging Configuration
        logging.basicConfig(filename='./logs/scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
        logging.info(msg='Now monitoring {}'.format(coin['name']))

        # Storing post
        base_url = "https://www.mintscan.io/"

        # Open website
        driver.get(coin["link"])
        WebDriverWait(driver, delay).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.FeaturedProposals_featuredProposalGrid__3pQ0-')))

        # Topmost Proposal
        latest_proposal = {
            'title' : driver.find_element(by=By.CSS_SELECTOR, value='div h2').text,
            'link': driver.find_element(by=By.CSS_SELECTOR, value='div.ProposalCard_rightArrowWrapper__3lX_p a.ProposalCard_link__38deC').get_attribute('href')
        }
        
        # First time scraping
        if coin["post"] == "":
            logging.info(msg="First time running {} monitor. Inserting a latest post...".format(coin["name"]))
            update_post(latest_proposal, coin['name'])
            return "New"
        elif json.loads(coin["post"]) == latest_proposal:
            logging.info(msg="{} hasn't updated yet. Moving onto next coin...".format(coin["name"]))
            return None
        else:
            logging.info(msg="{} has some updates. Now sharing via telegram...".format(coin["name"]))
            update_post(latest_proposal, coin['name'])

            # Return post to send telegram message
            latest_proposal['name'] = coin['name']
            return latest_proposal
    except Exception as e:
        logging.info(msg = e)
        raise Exception(e)

# Testing code
#mintscan_scrape(get_coin("ATOLO"))