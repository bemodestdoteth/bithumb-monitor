# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

# FreeProxy for preventing IP ban
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
import requests

# Import file from parent directory
from pathlib import Path
import json
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_coin, update_post
from dotenv import load_dotenv
import logging

# Environment Variables
load_dotenv()

def github_repo_scrape(coin):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    try:
        print('''
        \n-----------------------------------------
        NOW WATCHING {}\n-----------------------------------------\n
        '''.format(coin['name']))
        
        # Storing post
        base_address = 'https://github.com'

        # Logging Configuration
        logging.basicConfig(filename='./logs/scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
        logging.info(msg='Now monitoring {}'.format(coin['name']))

        # Configure user agent
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.COMPUTER]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

        # To-do: add https proxy suppport
        proxy = {'http': FreeProxy().get()}
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

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
            logging.info(msg="First time running {} monitor. Inserting file data...".format(coin["name"]))
            update_post(latest_files, coin['name'])
            s.close()
            return "New"
        elif json.loads(coin["post"]) == latest_files:
            logging.info(msg="{} hasn't updated yet. Moving onto next coin...".format(coin["name"]))
            s.close()
            return None
        else:
            logging.info(msg="{} has some updates. Now sharing via telegram...".format(coin["name"]))
            update_post(latest_files, coin['name'])
            s.close()
            # Return post to send telegram message
            return {'name': coin['name'], 'title': "See what has been committed in the link.", 'link': coin['link']}
    except Exception as e:
        logging.info(msg = e)
        raise Exception(e)