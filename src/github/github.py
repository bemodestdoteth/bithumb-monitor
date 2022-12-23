# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

# VPN for roataing IP Address
from bs4 import BeautifulSoup
from nordvpn_switcher import initialize_VPN, rotate_VPN, terminate_VPN
import requests

# FreeProxy for preventing IP ban
from fp.fp import FreeProxy

# Import file from parent directory
from pathlib import Path
import json
import os
import time
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_coin, update_post
from dotenv import load_dotenv
import logging

# Environment Variables
load_dotenv()

def prior_setup_bs4(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

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
        
        # Storing post
        base_address = 'https://github.com'

        # Logging Configuration
        logging.basicConfig(filename='./logs/scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
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
        if coin_info["post"] == "":
            logging.info(msg="First time running {} monitor. Inserting a latest post...".format(coin_info["name"]))
            update_post(latest_release, coin)
            s.close()
            return None
        elif json.loads(coin_info["post"]) == latest_release:
            logging.info(msg="{} hasn't updated yet. Moving onto next coin...".format(coin_info["name"]))
            s.close()
            return None
        else:
            logging.info(msg="{} has some updates. Now sharing via telegram...".format(coin_info["name"]))
            update_post(latest_release, coin)
            s.close()

            # Return post to send telegram message
            latest_release['name'] = coin
            print(latest_release)
            return latest_release
    except Exception as e:
        logging.info(msg = e)
        raise Exception(e)

# Testing code
for item in ['TFUEL']:
    github_scrape(item)

'''
settings = initialize_VPN(area_input=['South Korea, Japan, Taiwan, Hong Kong'])
while True:
    print('Working...')
    rotate_VPN(settings)
    time.sleep(10)
terminate_VPN(settings)
'''
