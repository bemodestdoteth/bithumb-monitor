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

# Environment Variables
load_dotenv()

# Configure user agent
software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.COMPUTER]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

# Random Proxy
proxy_obj = FreeProxy(rand=True)

# To-do: add https proxy suppport
coin = "EGLD"
proxy = {'http': proxy_obj.get()}
headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

# Logging Configuration
logging.basicConfig(filename='./src/github/github.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)

def get_coin(coin):
    # Import DB to get coin information
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    # params = os.path.basename(os.path.dirname(__file__))
    query = "SELECT * FROM coins WHERE name = ?"
    item = cur.execute(query, (coin,)).fetchone()
    return {
        "name": item[0],
        "link": item[1],
        "posts": item[2]}

def github_scrape(coin, headers, proxy):
    """Scrapes the Snipes site and adds each item to an array
    Args:
        headers (dict): {'User-Agent': ''}
        proxy (dict): {'http': '', 'https': ''}
    """

    print('''
        \n-----------------------------------------
        NOW WATCHING EGLD
        -----------------------------------------\n
        ''')
    logging.info(msg='Successfully started monitor')

    # Get coin infor from database
    coin_info = get_coin(coin)
    
    # Storing posts
    base_address = 'https://github.com/'
    posts = []
    
    # Make request to site
    s = requests.Session()
    html = s.get(coin_info["link"], headers=headers, proxies=proxy, verify=False, timeout=50)
    soup = BeautifulSoup(html.text, 'html.parser')
    array = soup.find_all(attrs={'data-test-selector':'release-card'})

    latest_post = {
        'title' : array[0].find(class_ = 'Link--primary').text,
        'link': base_address + array[0].a['href']
    }
    
    # First time scraping
    if coin_info["posts"] == "[]":
        for i in array:
            posts.append({
                'title' : i.find(class_ = 'Link--primary').text,
                'link': base_address + i.a['href']
            })
        posts.reverse()
        coin_info["posts"] = posts
    else:
        latest_post = coin_info["posts"][-1]
        

    logging.info(msg='Successfully scraped site.')
    s.close()
    return posts

github_scrape(coin, headers, proxy)