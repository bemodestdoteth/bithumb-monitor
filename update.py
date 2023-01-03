from datetime import datetime, timedelta
from db import get_all_coins, create_coins_db, create_xangle_rebrand_db, create_xangle_swap_db, create_proxy_db
from dotenv import load_dotenv
from config import print_n_log
import asyncio
import telegram
import time
import os

from src.github.github import github_scrape
from src.github_repo.github_repo import github_repo_scrape
from src.github_wiki.github_wiki import github_wiki_scrape
from src.icx_forum.icx_forum import icx_forum_scrape
from src.mintscan.mintscan import mintscan_scrape
from src.snx_blog.snx_blog import snx_blog_scrape
from src.xtz_agora.xtz_agora import xtz_agora_scrape
from src.xangle.xangle import xangle_scrape
from src.xangle.xangle_token_swap import xangle_token_swap_scrape
from src.xangle.xangle_token_rebrand import xangle_token_rebrand_scrape

load_dotenv()

def parse_markdown_v2(msg):
    reserved_words = ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!')
    for reserved_word in reserved_words:
        msg = msg.replace(reserved_word, "\{}".format(reserved_word))
    return msg
def scrape_func_selector(coin):
    try:
        if coin['source'] == "github-release":
            return github_scrape(coin)
        elif coin['source'] == "github-repo":
            return github_repo_scrape(coin)
        elif coin['source'] == "icx-forum":
            return icx_forum_scrape(coin)
        elif coin['source'] == "github-wiki":
            return github_wiki_scrape(coin)
        elif coin['source'] == "mintscan":
            return mintscan_scrape(coin)
        elif coin['source'] == "snx-blog":
            return snx_blog_scrape(coin)
        elif coin['source'] == "xangle":
            return xangle_scrape(coin)
        elif coin['source'] == "xtz-agora":
            return xtz_agora_scrape(coin)
        else:
            return "Pass"
    except Exception as e:
        raise Exception(e)
async def send_message(update_info):
    # Resolve reserved characters
    update_name = parse_markdown_v2(update_info['name'])
    update_title = parse_markdown_v2(update_info['title'])
    update_link = parse_markdown_v2(update_info['link'])

    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '__*🔔{} has a new update\!🔔*__\n{}\n{}\n'.format(update_name, update_title, update_link)
    await bot.sendMessage(chat_id=chat_id, text=msg, parseMode='markdownv2')
async def send_error_message(work, msg):
    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    msg_2 = "__*🚫An error occurred while working on {}\!\!🚫*__\n\n{}".format(parse_markdown_v2(work), parse_markdown_v2(msg))
    await bot.sendMessage(chat_id=chat_id, text=msg_2, parse_mode='markdownv2')    
def get_update():
    try:
        # Check db existence before beginning
        if not(os.path.isfile("coins.db")):
            print_n_log("No database detected. Creating new before moving on.")
            create_coins_db()
            create_xangle_swap_db()
            create_xangle_rebrand_db()
            create_proxy_db()
        while True:
            coins = get_all_coins()
            for coin in coins:
                result = scrape_func_selector(coin)
                if result is None:
                    print_n_log("{} has no further updates".format(coin['name']))
                elif result == "Pass":
                    print_n_log("Scraping {}: Not updated yet.".format(coin['name']))
                elif result == "New":
                    print_n_log("A new data has been inserted into {}".format(coin['name']))                
                else:
                    print_n_log("{} has some update. Sending via telegram message...".format(result['name']))
                    asyncio.run(send_message(result))

            # Look for xangle updates after looking through each token
            xangle_token_swap_scrape({
                "name": "TOKEN SWAP DISCLOSURE",
                "link": "https://xangle.io/insight/disclosure?category=token_swap",
                "selector": ".bc-insight-list-item-wrapper"})
            xangle_token_rebrand_scrape({
                "name": "TOKEN REBRAND DISCLOSURE",
                "link": "https://xangle.io/insight/disclosure?category=token_rebranding",
                "selector": ".bc-insight-list-item-wrapper"})

            # 30 min cooldown after a successful scraping.
            print_n_log("Website updating job finished. Next job is projected at {}".format(datetime.strftime(datetime.now() + timedelta(minutes=30), format="%Y/%m/%d %H:%M:%S")))
            time.sleep(1800)
    except Exception as e:
        print_n_log(e)
        asyncio.run(send_error_message(coin["name"], e))
        raise Exception(e)

# Test Function
if __name__ == "__main__":
    get_update()