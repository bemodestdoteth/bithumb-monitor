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
from config import prior_setup_bs4, print_n_log

@prior_setup_bs4
def github_scrape(coin, proxy):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    # Storing post
    base_url = 'https://github.com'

    # Make request to site
    s = requests.Session()
    
    html = s.get(coin["link"], proxies={"http": proxy}, verify=False, timeout=50)
    soup = BeautifulSoup(html.text, 'html.parser')

    # With 'latest' tag
    if coin["name"] == "XEC":
        latest_release = {
            'title' : soup.find('h1', attrs={"data-view-component": "true"}).text + " / Checkpoint every Nov 15th or May 15th, which is also around version 0.2x.5. Buy around then",
            'link': base_url + soup.select('li.breadcrumb-item a[aria-current="page"]')[0]['href']
        }
    else:
        latest_release = {
            'title' : soup.find('h1', attrs={"data-view-component": "true"}).text,
            'link': base_url + soup.select('li.breadcrumb-item a[aria-current="page"]')[0]['href']
        }

    s.close()
    
    # First time scraping
    if coin["post"] == "":
        update_post(latest_release, coin['name'])
        return "New"
    elif json.loads(coin["post"]) == latest_release:
        return None
    else:
        update_post(latest_release, coin['name'])
        # Return post to send telegram message
        latest_release['name'] = coin['name']
        return latest_release

if __name__ == "__main__":
    github_scrape(get_coin("XEC"))