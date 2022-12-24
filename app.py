from dotenv import load_dotenv
from status import get_status
from update import get_update
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import time

load_dotenv()

def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(get_status)
        executor.submit(get_update)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program")