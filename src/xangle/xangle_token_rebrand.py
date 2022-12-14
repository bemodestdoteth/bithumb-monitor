from selenium.webdriver.common.by import By

# Import file from parent directory
from pathlib import Path
import os
import sys
os.chdir(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))
sys.path.append(str(Path(os.path.dirname(__file__)).parent.parent.absolute()))

from db import get_ticker
from config import prior_setup_selenium, print_n_log
import sqlite3

def empty_database():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    db_records = cur.execute("SELECT name FROM xangle_token_rebrand").fetchall()
    if len(db_records) == 0:
        con.close()
        return True
    else:
        con.close()
        return False
@prior_setup_selenium
def xangle_token_rebrand_scrape(coin, driver, delay):
    '''
    Scrapes the site and changes database accordingly
    '''
    # First time scraping
    if empty_database():
        # Get records from the site
        items = driver.find_elements(by=By.CSS_SELECTOR, value='.bc-insight-list-item-wrapper')
        items_splitted = tuple(item.text.split('\n') for item in items)
        names = tuple(item[1] for item in items_splitted)
        posts = tuple(item[5] for item in items_splitted)
        dates = tuple(item[4] for item in items_splitted)
        links = tuple(item.get_attribute('href') for item in items)
        
        # Connect database and add records
        con = sqlite3.connect('coins.db')
        cur = con.cursor()
        query = "INSERT INTO xangle_token_rebrand VALUES (?, ?, ?, ?)"
        for i in range(len(names)):
            params = (names[i], posts[i], dates[i], links[i])
            cur.execute(query, params)
            con.commit()
    else:
        # Get records from the database
        con = sqlite3.connect('coins.db')
        cur = con.cursor()
        item_db = cur.execute("SELECT * FROM xangle_token_rebrand").fetchone()

        # Get records from the site
        item = driver.find_element(by=By.CSS_SELECTOR, value='.bc-insight-list-item-wrapper')
        item_rec = item.text.split('\n')
        item_link = item.get_attribute('href')
        item_site_comp = (item_rec[1], item_rec[5], item_rec[4], item_link)

        driver.quit()

        if item_db == item_site_comp:
            print_n_log(msg="No new coin rebrand disclosure on xangle.")
            return None
        # Should only pass coins listed on Bithumb
        elif item_db[0] in (item for sublist in get_ticker().values() for item in sublist):
            print_n_log(msg="New coin rebrand disclosure detected on xangle.")

            # Return post to send telegram message
            return {"name": item_site_comp[0], "title":item_site_comp[1], "link": item_site_comp[3] }
        else:
            print_n_log(msg="A new coin rebrand disclosure has been discovered, buy it hasn't been listed on Bithumb.")
            return None