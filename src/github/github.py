# VPN for roataing IP Address
from bs4 import BeautifulSoup
import requests

# Import file from parent directory
from pathlib import Path
import json
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_coin, update_post
from config import prior_setup_bs4
from dotenv import load_dotenv
import logging

# Environment Variables
load_dotenv()

@prior_setup_bs4
def github_scrape(coin, proxy, headers):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    try:        
        # Logging Configuration
        logging.basicConfig(filename='./logs/scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
        logging.info(msg='Now monitoring {}'.format(coin['name']))

        # Storing post
        base_url = 'https://github.com'

        # Make request to site
        s = requests.Session()
        
        html = s.get(coin["link"], headers=headers, proxies=proxy, verify=False, timeout=50)
        soup = BeautifulSoup(html.text, 'html.parser')
    
        # With 'latest' tag
        latest_release = {
            'title' : soup.find('h1', attrs={"data-view-component": "true"}).text,
            'link': base_url + soup.select('li.breadcrumb-item a[aria-current="page"]')[0]['href']
        }

        # First time scraping
        if coin["post"] == "":
            logging.info(msg="First time running {} monitor. Inserting a latest post...".format(coin["name"]))
            update_post(latest_release, coin['name'])
            s.close()
            return "New"
        elif json.loads(coin["post"]) == latest_release:
            logging.info(msg="{} hasn't updated yet. Moving onto next coin...".format(coin["name"]))
            s.close()
            return None
        else:
            logging.info(msg="{} has some updates. Now sharing via telegram...".format(coin["name"]))
            update_post(latest_release, coin['name'])
            s.close()

            # Return post to send telegram message
            latest_release['name'] = coin['name']
            return latest_release
    except Exception as e:
        logging.info(msg = e)
        raise Exception(e)
    
#github_scrape(get_coin('EGLD'))