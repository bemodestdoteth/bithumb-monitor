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
def github_repo_scrape(coin, proxy, headers):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    # Storing post
    base_address = 'https://github.com'

    # Make request to site
    s = requests.Session()

    html = s.get(coin["link"], headers=headers, proxies=proxy, verify=False, timeout=50)
    soup = BeautifulSoup(html.text, 'html.parser')

    # Fetch every file from the directory
    files = soup.select('a.js-navigation-open.Link--primary')
    names = tuple(file.text for file in files)
    links = tuple(base_address + file['href'] for file in files)

    # Fill as a json format
    latest_files = {}
    for i in range(len(names)):
        latest_files[str(i + 1)] = {
            "title": names[i],
            "link": links[i],
        }

    # First time scraping
    if coin["post"] == "":
        print_n_log(msg="First time running {} monitor. Inserting file data...".format(coin["name"]))
        update_post(latest_files, coin['name'])
        s.close()
        return "New"
    elif json.loads(coin["post"]) == latest_files:
        print_n_log(msg="{} hasn't updated yet. Moving onto next coin...".format(coin["name"]))
        s.close()
        return None
    else:
        print_n_log(msg="{} has some updates. Now sharing via telegram...".format(coin["name"]))
        update_post(latest_files, coin['name'])
        s.close()
        # Return post to send telegram message
        return {'name': coin['name'], 'title': "See what has been committed in the link.", 'link': coin['link']}