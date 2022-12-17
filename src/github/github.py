# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

# FreeProxy for preventing IP ban
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
import requests

from db import get_coin, change_post
from dotenv import load_dotenv
import json
import logging
import sqlite3
import os

# Environment Variables
load_dotenv()

def github_scrape(coin):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    try:
        # Get coin infor from database
        coin_info = get_coin(coin)

        print('''
        \n-----------------------------------------
        NOW WATCHING {}\n-----------------------------------------\n
        '''.format(coin_info['name']))
        
        # Storing posts
        base_address = 'https://github.com'

        # Logging Configuration
        logging.basicConfig(filename='./log/scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
        logging.info(msg='Now monitoring {}'.format(coin_info['name']))

        # Configure user agent
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.COMPUTER]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

        # Random Proxy
        proxy_obj = FreeProxy(rand=True)

        # To-do: add https proxy suppport
        proxy = {'http': proxy_obj.get()}
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

        # Make request to site
        s = requests.Session()
        
        html = s.get(coin_info["link"], headers=headers, proxies=proxy, verify=False, timeout=50)
        soup = BeautifulSoup(html.text, 'html.parser')
    
        # With 'latest' tag
        latest_release = {
            'title' : soup.find('h1', attrs={"data-view-component": "true"}).text,
            'link': base_address + soup.select('li.breadcrumb-item a[aria-current="page"]')[0]['href']
            #'title' : soup.find(class_ = 'Link--primary').text,
            #'link': base_address + soup.a['href']
        }

        # First time scraping
        if coin_info["posts"] == "":
            logging.info(msg="First time running {} monitor. Inserting latest posts...".format(coin_info["name"]))
            change_post(latest_release, coin)
            s.close()
            return None
        elif json.loads(coin_info["posts"]) == latest_release:
            logging.info(msg="{} hasn't updated yet. Moving onto next coin...".format(coin_info["name"]))
            s.close()
            return None
        else:
            logging.info(msg="{} has some updates. Now sharing via telegram...".format(coin_info["name"]))
            change_post(latest_release, coin)
            s.close()
            # Return post to send telegram message
            latest_release['name'] = coin
            print(latest_release)
            return latest_release
    except Exception as e:
        logging.info(msg = e)
        raise Exception(e)

# Testing code
github_scrape('EGLD')