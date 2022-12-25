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
def github_scrape(coin, proxy, headers):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
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
        update_post(latest_release, coin['name'])
        s.close()
        return "New"
    elif json.loads(coin["post"]) == latest_release:
        s.close()
        return None
    else:
        update_post(latest_release, coin['name'])
        s.close()

        # Return post to send telegram message
        latest_release['name'] = coin['name']
        return latest_release