# Random user agents to deceive server
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType, OperatingSystem

from datetime import datetome
import time

# FreeProxy for preventing IP ban
from fp.fp import FreeProxy
from pybithumb import Bithumb
import requests


from dotenv import load_dotenv
import json
import logging
import traceback
import sqlite3
import os

# Logging Configuration
logging.basicConfig(filename='bithunmb-gadoori.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)

# Environment Variables
load_dotenv()

def maedo(coin):
    bithumb = Bithumb(os.environ['CONNECT_KEY'], os.environ['SECRET_KEY'])

    # Get Coin Price
    df = bithumb.get_candlestick(coin, chart_intervals="3m")['close'].tail(2).to_list()
    
    # Calculate Price Difference
    # Abort Order if Price Volatility is too high
    delta = ((df[1] - df[0])/df[0])*100
    if delta > 0.05:
        print('Price volatility too high. Aborting Order...')
        return
    
    # Get Balance and Calculate Buying Amount
    # (총 잔고, 거래중인 암호화폐 수량, 보유 원화, 주문에 사용된 원화)
    balance = bithumb.get_balance(coin)
    krw_amount = balance[2]
    default_amount = 3000000
    if krw_amount <= 3000:
        print('Not enough KRW. Exiting...')
        return
    elif default_amount > krw_amount:
        default_amount = krw_amount - 3000 # Cushion for volatility

    amount = round(default_amount / df[1], 8)
    # Test Function
    #amount = round(3000 / df[1], 8)
    print(amount)

    # Buy Coin
    result = bithumb.buy_market_order(coin, amount, 'KRW')
    print(result)

def maedo(coin):
    bithumb = Bithumb(os.environ['CONNECT_KEY'], os.environ['SECRET_KEY'])

    # Get Balance and Selling Amount
    # (총 잔고, 거래중인 암호화폐 수량, 보유 원화, 주문에 사용된 원화)
    balance = bithumb.get_balance(coin)
    amount = balance[0]
    
    # Sell Coin
    if amount != 0:
        result = bithumb.sell_market_order(coin, amount, 'KRW')
        print(result)

def main():
    url = "https://api.bithumb.com/public/assetsstatus/ALL"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    api_n = json.loads(response.text)['data']

    with open('./status.json','r') as f:
        api_o = json.loads(f.readline())

    for key in api_n.keys():
        if key not in tuple(api_o.keys()):
            print('new coin')

        elif api_n[key] != api_o[key]:
            if api_n[key]['withdrawal_status'] == 0:
                print(api_n[key])
                print('{} withdrawal closed'.format(key))
                #if key in Bithumb.get_tickers():
                #    print('Buying {}...'.format(key))
                #    maesoo(key)
            elif api_n[key]['withdrawal_status'] == 1:
                print('{} withdrawal opened'.format(key))

    #with open('./status.json','w') as f:
    #    f.write(json.dumps(api_n))
        
#main()

df = Bithumb.get_tickers()
print(df)