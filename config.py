# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

# FreeProxy for preventing IP ban
from fp.fp import FreeProxy

from selenium import webdriver
import os

def prior_setup_bs4(func):
    def inner(coin):
        print('''
        \n-----------------------------------------
        NOW WATCHING {}\n-----------------------------------------\n
        '''.format(coin['name']))

        # Configure user agent
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.COMPUTER]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

        # To-do: add https proxy suppport
        proxy = {'http': FreeProxy().get()}
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
        return func(coin, proxy, headers)
    return inner
def prior_setup_selenium(func):
    def inner(coin):
        print('''
        \n-----------------------------------------
        NOW WATCHING {}\n-----------------------------------------\n
        '''.format(coin['name'])) 

        # To-do: add https proxy suppport
        proxy = {'http': FreeProxy().get()}

        # Open website
        driver = os_selection(user_agent=proxy)
        return func(coin, driver, delay = 5)
    return inner
def os_selection(user_agent):
    chrome_options = webdriver.ChromeOptions()
    # Selenium on Linux
    if os.name == 'posix':
        # To bypass headless block
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920, 1080')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument(f'user-agent={user_agent}')
    # Selenium on Windows
    elif os.name == 'nt':
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920, 1080')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument(f'user-agent={user_agent}')
        '''
        Add Extension to Chrome
        t.ly/wxZQ
        Preserve user cookies
        t.ly/uDkv
        '''
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def update_chromedriver():
    if os.name == 'posix': # Only on linux
        os.system('version=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE");wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip";sudo unzip -o /tmp/chromedriver_linux64.zip -d ~/usr/bin;rm /tmp/chromedriver_linux64.zip')