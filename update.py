from datetime import datetime, timedelta
from db import coins, get_coin, get_all_coins, create_coins_db, create_xangle_rebrand_db, create_xangle_swap_db
from dotenv import load_dotenv
from config import print_n_log
import asyncio
import telegram
import time
import os

from src.github.github import github_scrape
from src.github_repo.github_repo import github_repo_scrape
from src.mintscan.mintscan import mintscan_scrape
from src.xangle.xangle_token_swap import xangle_token_swap_scrape
from src.xangle.xangle_token_rebrand import xangle_token_rebrand_scrape

load_dotenv()

def scrape_func_selector(coin):
    try:
        if coin['source'] == "github-release":
            return github_scrape(coin)
        elif coin['source'] == "github-repo":
            return github_repo_scrape(coin)
        elif coin['source'] == "mintscan":
            return mintscan_scrape(coin)
        else:
            print_n_log("Scraping {}: Not updated yet.".format(coin['name']))
    except Exception as e:
        raise Exception(e)
async def send_message(update_info):
    # Resolve reserved characters
    update_name = update_info['name']
    update_title = update_info['title'].replace('.', '\.').replace('-', '\-')
    update_link = update_info['link'].replace('.', '\.').replace('-', '\-')

    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '🔔**{} has a new update\!**🔔\n**{}**\n**{}**\n'.format(update_name, update_title, update_link)
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')
def get_update():
    # Check db existence before beginning
    if not(os.path.isdir("coins.db")):
        print_n_log("No database detected. Creating new before moving on.")
        create_coins_db()
        create_xangle_swap_db()
        create_xangle_rebrand_db()
    while True:
        coins = get_all_coins()
        for coin in coins:
            result = scrape_func_selector(coin)
            if result is None:
                print_n_log("{} has no further updates".format(coin['name']))
            elif result == "New":
                print_n_log("A new data has been inserted into {}".format(coin['name']))                
            else:
                print_n_log("{} has some update. Sending via telegram message...".format(result['name']))
                asyncio.run(send_message(result))

        # Look for xangle updates after looking through each token
        xangle_token_swap_scrape("TOKEN SWAP DISCLOSURE")
        xangle_token_rebrand_scrape("TOKEN REBRAND DISCLOSURE")

        # 30 min cooldown after a successful scraping.
        print_n_log("Website updating job finished. Next job is projected at {}".format(datetime.strftime(datetime.now() + timedelta(minutes=30), format="%Y/%m/%d %H:%M:%S")))
        time.sleep(1800)