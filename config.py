from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

# FreeProxy for preventing IP ban
from fp.fp import FreeProxy

from db import get_working_proxy, write_proxy, delete_proxy
from selenium import webdriver
from datetime import datetime
import logging
import os

def prior_setup_bs4(func):
    def inner(coin):
        print("-----------------------------------------")
        print_n_log("NOW WATCHING {}".format(coin['name']))
        print("-----------------------------------------")

        # First time setting proxy
        if get_working_proxy() is None:
            proxl = FreeProxy(rand=True, https=True).get().replace("http://", "")
        else:
            proxl = get_working_proxy()

        print_n_log("Connected to: {}".format(proxl))
        return func(coin, proxl)
    return inner
def prior_setup_selenium(func):
    def inner(coin, delay = 10):
        print("-----------------------------------------")
        print_n_log("NOW WATCHING {}".format(coin['name']))
        print("-----------------------------------------")

        error_cnt = 0
        driver = ""

        # First time setting proxy
        if get_working_proxy() is None:
            proxl = FreeProxy(rand=True, https=True).get().replace("http://", "")
            print_n_log("Connected to: {}".format(proxl))
        else:
            proxl = get_working_proxy()
            print_n_log("Connected to: {}".format(proxl))        

        # Open website and handle errors
        while True:
            try:
                driver = os_selection(proxy = proxl)
                driver.get(coin['link'])
                WebDriverWait(driver, delay).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, coin["selector"])))
                write_proxy(proxl)
                break
            except TimeoutException:
                print_n_log("Connection with proxy failed for TimeoutException. Trying again...")
                if driver != "":
                    driver.quit()
                error_cnt = error_cnt + 1
                if error_cnt >= 3:
                    print_n_log("Changing proxy due to concurrent errors...")
                    delete_proxy(proxl)
                    
                    proxl = FreeProxy(rand=True, https=True).get().replace("http://", "")
                    print_n_log("Now connected to: {}".format(proxl))
                    error_cnt = 0
            except WebDriverException as e:
                print (e)
                print_n_log("Connection with proxy failed for WebDriverException. Trying again...")
                if driver != "":
                    driver.quit()
                error_cnt = error_cnt + 1
                if error_cnt >= 3:
                    print_n_log("Changing proxy due to concurrent errors...")
                    delete_proxy(proxl)
                    
                    proxl = FreeProxy(rand=True, https=True).get().replace("http://", "")
                    print_n_log("Now connected to: {}".format(proxl))
                    error_cnt = 0
        
        return func(coin, driver, delay)
    return inner
def os_selection(proxy):
    chrome_options = webdriver.ChromeOptions()
    # Selenium on Linux
    if os.name == 'posix':
        # Bypass headless block
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument('--window-size=1920, 1080')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        #chrome_options.add_argument(f'user-agent={user_agent}')
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
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
    driver = webdriver.Chrome(options=chrome_options)
    return driver
def update_chromedriver():
    if os.name == 'posix': # Only on linux
        os.system('version=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE");wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip";sudo unzip -o /tmp/chromedriver_linux64.zip -d /usr/bin;rm /tmp/chromedriver_linux64.zip')
def print_n_log(msg, is_error = False):
    if not(is_error):
        print("{}  {}".format(datetime.strftime(datetime.now(), format="%Y/%m/%d %H:%M:%S"), msg))
        logging.basicConfig(filename='./scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
        logging.info(msg)
    else:
        print("{}  Error: {}".format(datetime.strftime(datetime.now(), format="%Y/%m/%d %H:%M:%S"), msg))
        logging.basicConfig(filename='./scraping.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.ERROR)
        logging.error(msg)