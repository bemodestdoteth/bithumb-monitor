import sqlite3
import os
import json

'''
with open('./sample_db.json','r') as f:
    coins = json.loads(f.readline())
'''
def create_coins_db(coins):
    if not(os.path.isfile('coins.db')):
        con = sqlite3.connect('coins.db')
        cur = con.cursor()

        # Create table
        cur.execute("CREATE TABLE coins (name PRIMARY KEY, link NOT NULL, posts)")
        con.commit()

        # insert first values
        insert_coin(coins)

def insert_coin(coins):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "INSERT INTO coins VALUES (?, ?, ?)"

    for coin in coins.items():
        params = list((coin[0], coin[1]["link"], coin[1]["posts"]))
        cur.execute(query, params)
    con.commit()

def get_coin(coin):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "SELECT * FROM monitors WHERE name = ?"
    params = coin
    item = cur.execute(query, params)
    try:
        for i in item:
            return i
    except:
        return None

# Need revision, low priority
def update_config(coin, name=None, link=None, delay=None, details=None):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = 'UPDATE monitors SET '
    start = 0
    empty = True
    for col in columns:
        if eval(col) == 'null':
            if start == 0:
                query += f"{col} = null"
                start = 1
                empty=False
            else:
                query += f", {col} = null"
        elif eval(col) is not None:
            if start == 0:
                query += f"{col} = '{eval(col)}'"
                start = 1
                empty=False
            else:
                query += f", {col} = '{eval(col)}'"
        elif eval(col) == None:
            pass

    query += f" WHERE name = '{coin}';"
    print(query)
    if empty is False:
        cur.execute(query)
        con.commit()


def get_all_coins():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    item = cur.execute("SELECT * FROM coins;")
    try:
        items = []
        for i in item:
            items.append(i)
        return items
    except:
        return None

coins = {
    "META": {
    "link": "https://brunch.co.kr/magazine/metadium-info",
    "posts": ""
    },
    "EGLD": {
    "link": "https://github.com/ElrondNetwork/elrond-go/releases",
    "posts": ""
    },
    "THETA": {
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases",
    "posts": ""
    },
    "TFUEL": {
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases",
    "posts": ""
    },
    "TDROP": {
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases",
    "posts": ""
    }}

create_coins_db(coins)