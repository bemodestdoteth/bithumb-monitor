from db import get_coin, get_all_coins
from dotenv import load_dotenv
from status import get_status
from github import github
from github_repo import github_repo
import asyncio
import telegram
import os

load_dotenv()

def scrape_func_selector(coin):
    if coin['source'] == "github":
        return github.github_scrape(coin)
    elif coin['source'] == "github-repo":
        return github_repo.github_repo_scrape(coin)
    elif coin['source'] == "github-repo":
        return github_repo.github_repo_scrape(coin)
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
    coins = get_all_coins()
    for coin in coins:
        result = scrape_func_selector(coin)
        if result is not None:
            print("{} has some update. Sending via telegram message...".format(result['name']))
            asyncio.run(send_message(result))
        else:
            print("{} has no further updates".format(coin['name']))

get_update()