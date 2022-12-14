import sqlite3
import os
import json

with open('./sample_db.json','r') as f:
    coins = json.loads(f.readline())

def create_coins_db():
    if os.path.isfile('coins.db'):
        con = sqlite3.connect('coins.db')
    else: # No file
        con = sqlite3.connect('coins.db')
        cur = con.cursor()
        cur.execute("create table coins (name, link, posts)")
        
        query = "INSERT INTO coins VALUES (?, ?, ?)"

        for coin in coins:
            params = tuple(coin, coin["link"], coin["posts"])
            cur.execute(query, params)
        con.commit()

def get_config(coin):
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


def get_all_config():
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
    
create_coins_db()