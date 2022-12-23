from selenium import webdriver
import os

def os_selection(user_agent):
    chrome_options = webdriver.ChromeOptions()
    # Selenium on Linux
    if os.name == 'posix':
        # To bypass headless block
        user_agent = 'Chrome/102.0.5005.61'
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
    driver = webdriver.Chrome(options=chrome_options, executable_path=os.path.join(os.path.dirname(__file__), 'chromedriver'))
    return driver