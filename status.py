# FreeProxy for preventing IP ban
from fp.fp import FreeProxy

# FreeProxy for preventing IP ban
from pybithumb import Bithumb
from dotenv import load_dotenv
from db import get_all_coins
from config import print_n_log
from db import get_working_proxy

import json
import logging
import os
import requests
import time

# Environment Variables
load_dotenv()

def maesoo(coin): # Not using right now
    bithumb = Bithumb(os.environ['CONNECT_KEY'], os.environ['SECRET_KEY'])

    # Get Coin Price
    df = bithumb.get_candlestick(coin, chart_intervals="3m")['close'].tail(2).to_list()
    
    # Calculate Price Difference
    # Abort Order if Price Volatility is too high
    delta = ((df[1] - df[0])/df[0])*100
    if delta > 0.05:
        print_n_log('Price volatility too high. Aborting Order...')
        return
    
    # Get Balance and Calculate Buying Amount
    # (총 잔고, 거래중인 암호화폐 수량, 보유 원화, 주문에 사용된 원화)
    balance = bithumb.get_balance(coin)
    krw_amount = balance[2]
    default_amount = 3000000
    if krw_amount <= 3000:
        print_n_log('Not enough KRW. Exiting...')
        return
    elif default_amount > krw_amount:
        default_amount = krw_amount - 3000 # Cushion for volatility

    amount = round(default_amount / df[1], 8)
    # Test Function
    #amount = round(3000 / df[1], 8)
    print_n_log(amount)

    # Buy Coin
    result = bithumb.buy_market_order(coin, amount, 'KRW')
    print_n_log(result)
def maedo(coin):
    bithumb = Bithumb(os.environ['BITHUMB_CONNECT_KEY'], os.environ['BITHUMB_SECRET_KEY'])

    # Get Balance and Selling Amount
    # (총 잔고, 거래중인 암호화폐 수량, 보유 원화, 주문에 사용된 원화)
    balance = bithumb.get_balance(coin)
    if balance["status"]:
        print_n_log("Couldn't connect to Bithumb API. Skip Selling...")        
    else:
        amount = balance[0]
        # Sell Coin
        if amount > 0:
            # Wait for other bot and person buying up coins
            time.sleep(10)
            result = bithumb.sell_market_order(coin, amount, 'KRW')
            print_n_log(result)
        else:
            print_n_log('You don\'t hane {} in your balances. Skip selling...'.format(coin))
def get_ticker():
    tickers = {}
    omits = ['BTC', 'ETH', 'XRP', 'BCH', 'EOS', 'TRX']
    tickers["KRW"] = Bithumb.get_tickers('KRW')
    tickers["BTC"] = list((btc_ticker for btc_ticker in Bithumb.get_tickers('btc') if btc_ticker not in tickers['KRW']))
    return tickers
def get_buy_sell_coins():
    coin_list = []
    for coin in get_all_coins():
        if coin["groups"] != "":
            (coin_list.append(*group) for group in coin["groups"].split(","))
        else:
            coin_list.append(coin["name"])
    return coin_list
def get_status():
    url = "https://api.bithumb.com/public/assetsstatus/ALL"
    headers = {"accept": "application/json"}

    proxy_timer = 0
    ticker_timer = 0
    proxy = get_working_proxy()
    #tickers = get_ticker()
    coin_list = get_buy_sell_coins()

    while True:
        try:
            response = requests.get(url,proxies={"http": proxy}, headers=headers)
            api_n = json.loads(response.text)['data']

            # If there's no status.json, skip the whole process and save the first result as status.json
            if os.path.isfile('./status.json'):
                with open('./status.json','r') as f:
                    api_o = json.loads(f.readline())

                for coin in api_n.keys():
                    if coin not in tuple(api_o.keys()):
                        print_n_log('New coin: {}'.format(coin))

                    elif api_n[coin] != api_o[coin]:
                        if api_n[coin]['withdrawal_status'] == 0:
                        #if api_n[coin]['withdrawal_status'] == 1:
                            if coin in coin_list:
                                print_n_log('{} withdrawal closed.'.format(coin, coin))
                                maedo(coin)
                        elif api_n[coin]['withdrawal_status'] == 0:
                            if coin in coin_list:
                                print_n_log('{} withdrawal opened'.format(coin))
                                #print_n_log('Selling {}...'.format(coin))
                                #maesoo(coin)

            with open('./status.json','w') as f:
                f.write(json.dumps(api_n))
                print_n_log(msg='Suucessfully fetched deposit and withdraw status.')
                        
            ticker_timer = ticker_timer + 1
            proxy_timer = proxy_timer + 1

            # Get ticker every hour
            if ticker_timer >= 1800:
                print_n_log('Ticker checking timer reached. Updating ticker...')
                tickers = get_ticker()
                ticker_timer = 0
            # Change proxy every 10 minutes
            if proxy_timer >= 300:
                print_n_log('Proxy change timer reached. Changing proxy...')
                proxy = get_working_proxy()
                print_n_log('Proxy changed. A new proxy is: {}'.format(proxy))
                proxy_timer = 0

            time.sleep(2)
        except Exception as e:
            logging.info(e)
            raise Exception(e)
            break

#get_status()