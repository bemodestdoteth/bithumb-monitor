from db import get_coin, get_all_coins
from dotenv import load_dotenv
from status import get_status
from src.github.github import github_scrape
from src.github_repo.github_repo import github_repo_scrape
from src.mintscan.mintscan import mintscan_scrape
import asyncio
import telegram
import time
import os

load_dotenv()

def scrape_func_selector(coin):
    try:
        if coin['source'] == "github-release":
            return github_scrape(coin)
        elif coin['source'] == "github-repo":
            return github_repo_scrape(coin)
        elif coin['source'] == "mintscan":
            return mintscan_scrape(coin)
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
    while True:
        coins = get_all_coins()
        for coin in coins:
            result = scrape_func_selector(coin)
            if result is not None:
                print("{} has some update. Sending via telegram message...".format(result['name']))
                asyncio.run(send_message(result))
            else:
                print("{} has no further updates".format(coin['name']))

        # 30 min cooldown after a successful scraping.
        time.sleep(1800)

get_update()