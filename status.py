# FreeProxy for preventing IP ban
from apscheduler.schedulers.background import BackgroundScheduler
from pybithumb import Bithumb
from dotenv import load_dotenv

import json
import logging
import os
import requests
import time

# Logging Configuration
logging.basicConfig(filename='bithumb_status.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG)

# Environment Variables
load_dotenv()

def maesoo(coin):
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
    bithumb = Bithumb(os.environ['BITHUMB_CONNECT_KEY'], os.environ['BITHUMB_SECRET_KEY'])

    # Get Balance and Selling Amount
    # (총 잔고, 거래중인 암호화폐 수량, 보유 원화, 주문에 사용된 원화)
    balance = bithumb.get_balance(coin)
    amount = balance[0]

    # Sell Coin
    if amount > 0:
        result = bithumb.sell_market_order(coin, amount, 'KRW')
        print(result)
    else:
        print('You don\'t hane {} in your balances. Skipping selling...'.format(coin))
def get_status():
    url = "https://api.bithumb.com/public/assetsstatus/ALL"
    headers = {"accept": "application/json"}

    while True:
        try:
            response = requests.get(url, headers=headers)
            api_n = json.loads(response.text)['data']

            with open('./status.json','r') as f:
                api_o = json.loads(f.readline())

            for coin in api_n.keys():
                if coin not in tuple(api_o.keys()):
                    print('New coin: {}'.format(coin))

                elif api_n[coin] != api_o[coin]:
                    #if api_n[coin]['withdrawal_status'] == 0:
                    if api_n[coin]['withdrawal_status'] == 1:
                        if coin in Bithumb.get_tickers():
                            print('{} withdrawal closed. Selling {}...'.format(coin, coin))
                            maedo(coin)
                    elif api_n[coin]['withdrawal_status'] == 0:
                        if coin in Bithumb.get_tickers():
                            print('{} withdrawal opened'.format(coin))
                            print('Selling {}...'.format(coin))
                            #maesoo(coin)

            with open('./status.json','w') as f:
                f.write(json.dumps(api_n))
                logging.info(msg='Suucessfully fetched deposit and withdraw status.')
                print('Sucessfully fetched deposit and withdraw status.')
            time.sleep(2)
        except Exception as e:
            logging.info(e)
            break

try:
    get_status()
except Exception as e:
    print(e)