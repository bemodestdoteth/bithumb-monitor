from selenium import webdriver
import os

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
# Change to a synchronous activity
def update_chromedriver():
    if os.name == 'posix': # Only on linux
        os.system('version=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") & wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip" & sudo unzip -o /tmp/chromedriver_linux64.zip -d ~/works/python-bithumb-monitor')