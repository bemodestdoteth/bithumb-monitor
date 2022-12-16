from dotenv import load_dotenv
from status import get_status
from update import get_update
from concurrent.futures import ThreadPoolExecutor
import time
import logging
import os

load_dotenv()

with ThreadPoolExecutor(max_workers=2) as executor:
    status_thread = threading.Thread(target=get_status, name='Get deposit and withdraw status from bithumb,')
    update_thread = threading.Thread(target=get_update, name='Get latest coin network update from its dev site.')