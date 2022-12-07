# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

from datetime import datetime
import time

# FreeProxy for preventing IP ban
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
import requests
import urllib3

from dotenv import load_dotenv
from pybithumb import Bithumb
import json
import logging
import traceback
import sqlite3
import os

# Import DB for comparison
con = sqlite3.connect(os.path.abspath('config.db'))
cur = con.cursor()
query = "SELECT * FROM coins WHERE name = ?"
params = os.path.basename(os.path.dirname(__file__))
#item = cur.execute(query, params)

# Environment Variables
load_dotenv()

# Logging Configuration
logging.basicConfig(filename='{}.log'.format(params), filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)

# Configure user agent
software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.COMPUTER]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

# Random Proxy
proxy_obj = FreeProxy(rand=True)

def scrape_main_site(github_release_site, headers, proxy):
    """Scrapes the Snipes site and adds each item to an array
    Args:
        headers (dict): {'User-Agent': ''}
        proxy (dict): {'http': '', 'https': ''}
    """
    
    base_address = 'https://github.com/'
    items = []
    
    # Make request to site
    s = requests.Session()
    html = s.get(github_release_site, headers=headers, proxies=proxy, verify=False, timeout=50)
    soup = BeautifulSoup(html.text, 'html.parser')
    array = soup.find_all(attrs={'data-test-selector':'release-card'})
    
    for i in array:
        item = {
            'title' : i.find(class_ = 'Link--primary').text,
            'link': base_address + i.a['href']
        }
        print(item)
        items.append(item)

    logging.info(msg='Successfully scraped site.')
    s.close()
    return items

def checker(item, start):
    if True:
        if start == 0:
            print('send telegram message')

def monitor():
    """
    Initiates monitor for github repo
    """
    print('''
        \n-----------------------------------------
        NOW WATCHING EGLD
        -----------------------------------------\n
        ''')
    logging.info(msg='Successfully started monitor')
    
    #proxy_https = proxy.replace('http', 'https')
    
    site = 'https://github.com/ElrondNetwork/elrond-go/releases'
    # To-do: add https proxy suppport
    proxy = {'http': proxy_obj.get()}
    headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
    
    scrape_main_site(site, headers, proxy)
    
monitor()