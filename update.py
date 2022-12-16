from dotenv import load_dotenv
from status import get_status
import asyncio
import telegram
import os

load_dotenv()

def get_update():
    # Todo
    asyncio.run(send_message("EGLD", {"title": "v1.3.51 - devnet hardfork 1", "link": "https://github.com/ElrondNetwork/elrond-go/releases/tag/v1.3.51-hf01"}))
async def send_message(coin_name, update_info):
    # Resolve reserved characters
    update_title = update_info['title'].replace('.', '\.').replace('-', '\-')
    update_link = update_info['link'].replace('.', '\.').replace('-', '\-')

    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '🔔**{} has a new update\!**🔔\n**{}**\n**{}**\n'.format(coin_name, update_title, update_link)
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')

get_update()