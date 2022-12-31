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

@prior_setup_bs4
def github_wiki_scrape(coin, proxy, headers):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    # Storing post
    base_url = 'https://github.com'

    # Make request to site
    s = requests.Session()

    html = s.get(coin["link"], headers=headers, proxies={"http": proxy}, verify=False, timeout=50)
    soup = BeautifulSoup(html.text, 'html.parser')

    file = soup.select('a.flex-1.py-1.text-bold')[-1]
    latest_files = {
        'title' : file.text,
        'link': base_url + file['href']
    }

    # First time scraping
    if coin["post"] == "":
        update_post(latest_files, coin['name'])
        s.close()
        return "New"
    elif json.loads(coin["post"]) == latest_files:
        s.close()
        return None
    else:
        update_post(latest_files, coin['name'])
        s.close()

        # Return post to send telegram message
        latest_files['name'] = coin['name']
        return latest_files

# Test Code
#github_wiki_scrape(get_coin("CSPR"))