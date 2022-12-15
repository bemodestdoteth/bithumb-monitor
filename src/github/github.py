# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

# FreeProxy for preventing IP ban
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
import requests

from dotenv import load_dotenv
import json
import logging
import sqlite3
import os

# Environment Variables
load_dotenv()

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

def change_post(post, coin):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET posts = ? WHERE name = ?"
    cur.execute(query, (json.dumps(post), coin))
    con.commit()

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
        logging.basicConfig(filename='./scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
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
        array = soup.find_all(attrs={'data-test-selector':'release-card'})

        latest_post = {
            'title' : array[0].find(class_ = 'Link--primary').text,
            'link': base_address + array[0].a['href']
        }

        # First time scraping
        if coin_info["posts"] == "":
            logging.info(msg="First time running {} monitor. Inserting latest posts...".format(coin_info["name"]))
            change_post(latest_post, coin)
            s.close()
            return None
        elif json.loads(coin_info["posts"]) == latest_post:
            logging.info(msg="{} hasn't updated yet. Moving onto next coin...".format(coin_info["name"]))
            s.close()
            return None
        else:
            logging.info(msg="{} has some updates. Now sharing via telegram...".format(coin_info["name"]))
            change_post(latest_post, coin)
            s.close()
            # Return post to send telegram message
            return latest_post
    except Exception as e:
        logging.info(msg = e)

coins = ["EGLD", "THETA", "TFUEL", "TDROP"]
for coin in coins:
    github_scrape(coin)