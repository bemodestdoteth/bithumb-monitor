# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

# FreeProxy for preventing IP ban
from fp.fp import FreeProxy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_config import os_selection

#from status import get_ticker
from dotenv import load_dotenv
import json
import logging
import os
import sys
import time

# Adding system path for import

# Environment Variables
load_dotenv()

url = "https://xangle.io/insight/disclosure?category=token_swap"

def xangle_token_swap_scrape(coin):
    '''
    Scrapes the site change database accordingly
    
    Parameters:
        coin (str) -- Name of the coin
    '''
    try:
        # Get coin infor from database
        print('''
        \n-----------------------------------------
        NOW WATCHING XANGLE TOKEN SWAP DISCLOSURE\n-----------------------------------------\n
        ''')
        
        # Storing posts
        base_address = 'https://xangle.io'

        # Logging Configuration
        logging.basicConfig(filename='./log/scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)
        logging.info(msg='Now monitoring xangle token swap disclosure...')

        # Configure user agent
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.COMPUTER]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

        # Random Proxy
        proxy_obj = FreeProxy(rand=True)

        # To-do: add https proxy suppport
        proxy = {'http': proxy_obj.get()}
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

        # Open driver and
        driver = os_selection()
        driver.get(url)
        
        '''
        soup = BeautifulSoup(html.text, 'html.parser')
        print(soup.find_all(True))
    
        # With 'latest' tag
        latest_release = {
            'title' : soup.find(class_=".bc-insight-list-item-area").text,
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
            return latest_release
        '''        
    except Exception as e:
        logging.info(msg = e)
        raise Exception(e)

# Testing code
#xangle_token_swap_scrape()

# Random Proxy
proxy_obj = FreeProxy(rand=True)

# To-do: add https proxy suppport
proxy = {'http': proxy_obj.get()}
print(proxy_obj)
print(proxy)

driver = os_selection(user_agent=proxy)