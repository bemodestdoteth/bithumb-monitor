from pybithumb import Bithumb
from dotenv import load_dotenv
from db import get_working_proxy, get_ticker, get_buy_sell_coins
from fp.fp import FreeProxy
from config import print_n_log
from update import send_error_message, send_buy_sell_message

import asyncio
import gc
import json
import os
from requests.exceptions import ConnectionError
import requests
import time

# Environment Variables
load_dotenv()

def get_ticker():
    tickers = {}
    omits = ['BTC', 'ETH', 'XRP', 'BCH', 'EOS', 'TRX']
    tickers["KRW"] = Bithumb.get_tickers('KRW')
    tickers["BTC"] = list((btc_ticker for btc_ticker in Bithumb.get_tickers('btc') if btc_ticker not in tickers['KRW']))
    return tickers
def get_balances(bithumb, coin):
    # (총 잔고, 거래중인 암호화폐 수량, 보유 원화, 주문에 사용된 원화)
    balance = bithumb.get_balance(coin)
    # Error moment
    if type(balance) is dict:
        msg = "Couldn't fetch balance for coins.\nReason: {}".format(balance["message"])
        asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", msg))
        print_n_log(msg)
        raise Exception(msg)
    else:
        return balance
def buy_market_orders(bithumb, coin, price, amount, market):
    print(coin, price, amount, market)
    result = bithumb.buy_market_order(coin, amount, market)
    # Error moment
    if type(result) is dict:
        msg = "Couldn't buy coins.\nReason: {}".format(result["message"])
        asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", msg))
        print_n_log(msg)
        raise Exception(msg)
    else:
        asyncio.run(send_buy_sell_message(result[0], result[1], price, amount))
def sell_market_orders(bithumb, coin, price, amount, market):
    result = bithumb.sell_market_order(coin, amount, market)
    # Error moment
    if type(result) is dict:
        msg = "Couldn't sell coins.\nReason: {}".format(result["message"])
        asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", msg))
        print_n_log(msg)
        raise Exception(msg)
    else:
        asyncio.run(send_buy_sell_message(result[0], result[1], price, amount))
def maesoo(coin, btc_market_coin):
    bithumb = Bithumb(os.environ['BITHUMB_CONNECT_KEY'], os.environ['BITHUMB_SECRET_KEY'])

    # Get Coin Price
    if coin in btc_market_coin:
        latest_price = bithumb.get_orderbook(coin, payment_currency="BTC")["asks"][0]["price"]
        price = tuple(bithumb.get_candlestick(coin, payment_currency="BTC", chart_intervals="1m")['close'].tail(1))[0]
    else:
        latest_price = bithumb.get_orderbook(coin, payment_currency="KRW")["asks"][0]["price"]
        price = tuple(bithumb.get_candlestick(coin, payment_currency="KRW", chart_intervals="1m")['close'].tail(1))[0]

    # Calculate Price Difference
    # Abort Order if Price Volatility is too high (current parameter: 5%)
    if abs(((latest_price - price)/price)*100) >= 5:
        msg = "Price volatility too high. Aborting Order..."
        asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", msg))
        print_n_log(msg)
    else:
        # Get Balance and Calculate Buying Amount
        krw_balance = get_balances(bithumb, coin)[2]
        #default_amount = 3000000
        default_amount = 3
        if krw_balance - 100 <= default_amount:
            msg = "Not enough KRW to buy coins."
            asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", msg))
            print_n_log(msg)
        else:
            # Buy Coin
            if coin in btc_market_coin:
                btc_price = bithumb.get_orderbook("BTC")["asks"][0]["price"]
                btc_amount = round(11100 / btc_price, 8)
                buy_market_orders(bithumb, "BTC", btc_price, btc_amount, 'KRW')
                # Minimum order amount: 0.0005
                amount = round(11000 / (price * btc_price), 8)
                buy_market_orders(bithumb, coin, price, amount, 'BTC')
            else:
                # Minimum order amount: 1,000 KRW
                amount = round(3000 / price, 8)
                buy_market_orders(bithumb, coin, price, amount, 'KRW')
def maedo(coin, btc_market_coin):
    bithumb = Bithumb(os.environ['BITHUMB_CONNECT_KEY'], os.environ['BITHUMB_SECRET_KEY'])

    # Get Balance and Selling Amount
    amount = get_balances(bithumb, coin)[0]
    if coin in btc_market_coin:
        price = bithumb.get_orderbook(coin, payment_currency="BTC")["bids"][0]["price"]
        btc_price = bithumb.get_orderbook("BTC")["bids"][0]["price"]
        krw_balance = amount * price * btc_price
    else:
        price = bithumb.get_orderbook(coin, payment_currency="KRW")["bids"][0]["price"]
        krw_balance = amount * price

    # Denominate coin balance in KRW to count in garbage amount like 50 KRW
    if krw_balance < 100:
        print_n_log('You don\'t have enough {} to sell in your balances. Skip selling...'.format(coin))
    else:
        # Wait for other bot and person buying up coins
        #time.sleep(10)
        if coin in btc_market_coin:
            sell_market_orders(bithumb, coin, price, amount, 'BTC')
            btc_received = get_balances(bithumb, "BTC")[0]
            sell_market_orders(bithumb, "BTC", btc_price, btc_received, 'KRW')
        else:
            sell_market_orders(bithumb, coin, price, amount, 'KRW')
def get_status():
    url = "https://api.bithumb.com/public/assetsstatus/ALL"
    headers = {"accept": "application/json"}

    # Initialize
    file_changed = False
    proxy_timer = 0
    proxy = get_working_proxy()
    btc_market_coin = get_ticker()["BTC"]

    # Get old api result before moving onto the loop for efficiency
    with open('./status.json','r') as f:
        api_o = json.loads(f.readline())

    while True:
        try:
            # If there's no status.json, skip the whole process and save the first result as status.json
            if file_changed and os.path.isfile('./status.json'):
                with open('./status.json','r') as f:
                    print_n_log(msg='Renewing api_o file since deposit and withdraw status has renewed...')
                    api_o = json.loads(f.readline())
                    file_changed = False

            # Get new data from Bithumb API
            api_n = json.loads(requests.get(url ,proxies={"http": proxy}, headers=headers).text)['data']

            if api_n != api_o:
                for coin in api_n.keys():
                    if coin not in tuple(api_o.keys()):
                        print_n_log('New coin: {}'.format(coin))
                    elif api_n[coin] != api_o[coin] and api_n[coin]['withdrawal_status'] == 0:
                        print_n_log('{} withdrawal closed.'.format(coin, coin))
                        maedo(coin, btc_market_coin)
                with open('./status.json','w') as f:
                    f.write(json.dumps(api_n))
                    file_changed = True
                    print_n_log(msg='Suucessfully renewed deposit and withdraw status.')
            else:
                print_n_log(msg='Keep watching deposit and withdraw status...')

            gc.collect()
            proxy_timer = proxy_timer + 1

            # Change proxy and get new ticker every 8 hours
            if proxy_timer >= 14400:
                print_n_log('Proxy change timer reached. Changing proxy...')
                proxy = FreeProxy(rand=True).get().replace("http://", "")
                print_n_log("Now Connected to: {}".format(proxy))
                btc_market_coin = get_ticker()["BTC"]              
                proxy_timer = 0
            time.sleep(2)
        except ConnectionError as e:
            asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", "Failed to fetch api. Changing proxy and try again...\n\nDetailed message: {}".format(e)))
            print_n_log("Failed to fetch api. Changing proxy and try again...")
            proxy = FreeProxy(rand=True).get().replace("http://", "")
            print_n_log("Now Connected to: {}".format(proxy))
        except Exception as e:
            asyncio.run(send_error_message("Bithumb Deposit and Withdraw Status", e))
            print_n_log(e)
            raise Exception(e)

if __name__ == "__main__":
    bithumb = Bithumb(os.environ['BITHUMB_CONNECT_KEY'], os.environ['BITHUMB_SECRET_KEY'])
    get_status()