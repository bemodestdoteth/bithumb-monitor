from pybithumb import Bithumb
import sqlite3
import os
import json
import random

def create_coins_db():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()

    # Create table
    cur.execute("CREATE TABLE coins (name PRIMARY KEY, source NOT NULL, link NOT NULL, selector, post, groups)")
    con.commit()

    # insert first values
    query = "INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?)"
    for coin in coins.items():
        params = list((coin[0], coin[1]["source"], coin[1]["link"], coin[1]["selector"], coin[1]["post"], coin[1]["groups"]))
        cur.execute(query, params)
    con.commit()
def create_xangle_swap_db():
    # Should only operate if coin db is created
    if os.path.isfile('coins.db'):
        con = sqlite3.connect('coins.db')
        cur = con.cursor()

        # Create table
        cur.execute("CREATE TABLE xangle_token_swap (name NOT NULL, post NOT NULL, date NOT NULL, link NOT NULL)")
        con.commit()
def create_xangle_rebrand_db():
    # Should only operate if coin db is created
    if os.path.isfile('coins.db'):
        con = sqlite3.connect('coins.db')
        cur = con.cursor()

        # Create table
        cur.execute("CREATE TABLE xangle_token_rebrand (name NOT NULL, post NOT NULL, date NOT NULL, link NOT NULL)")
        con.commit()
def create_proxy_db():
    # Should only operate if coin db is created
    if os.path.isfile('coins.db'):
        con = sqlite3.connect('coins.db')
        cur = con.cursor()

        # Create table
        cur.execute("CREATE TABLE working_proxy (proxy)")
        con.commit()    
def insert_coin(coins):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?)"

    for coin in coins.items():
        params = list((coin[0], coin[1]["source"], coin[1]["link"], coin[1]["selector"], coin[1]["post"], coin[1]["groups"]))
        cur.execute(query, params)
    con.commit()
def get_coin(coin):
    # Import DB to get coin information
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    query = "SELECT * FROM coins WHERE name = ?"
    item = cur.execute(query, (coin,)).fetchone()
    return {
        "name": item[0],
        "source": item[1],
        "link": item[2],
        "selector": item[3],
        "post": item[4],
        "groups": item[5]}
def get_all_coins():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    item = cur.execute("SELECT * FROM coins;")
    try:
        res = []
        for i in item:
            res.append({
            "name": i[0],
            "source": i[1],
            "link": i[2],
            "selector": i[3],
            "post": i[4],
            "groups": i[5]})
        return res
    except:
        return None
def get_ticker():
    tickers = {}
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
def get_working_proxy():
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    proxls = cur.execute("SELECT * FROM working_proxy").fetchall()
    if len(proxls) != 0:
        return proxls[random.randint(0, len(proxls) - 1)][0]
    else:
        return None
def write_proxy(proxy):
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    query = "INSERT INTO working_proxy VALUES (?)"
    cur.execute(query, (proxy, ))
    con.commit()
def delete_proxy(proxy):
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    query = "DELETE FROM working_proxy WHERE proxy = ?"
    cur.execute(query, (proxy, ))
    con.commit()
def update_post(post, coin):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET post = ? WHERE name = ?"
    cur.execute(query, (json.dumps(post), coin))
    con.commit()
def overhaul_post(coin, name):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET source = ?, link = ?, selector = ?, post = ?, groups = ? WHERE name = ?"
    cur.execute(query, (coin['source'], coin['link'], coin['selector'], coin['post'], coin['groups'], name))
    con.commit()

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

coins = {
    "META": {
    "source": "brunch",
    "link": "https://brunch.co.kr/magazine/metadium-info",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "EGLD": {
    "source": "github-release",
    "link": "https://github.com/ElrondNetwork/elrond-go/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "THETA": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "TFUEL": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "TDROP": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "CTXC": {
    "source": "github-release",
    "link": "https://github.com/CortexFoundation/CortexTheseus/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "MEDI": {
    "source": "github-repo",
    "link": "https://github.com/medibloc/panacea-governance/tree/main/proposals",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "XYM": {
    "source": "github-release",
    "link": "https://github.com/symbol/symbol/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },
    "ATOLO": {
    "source": "mintscan",
    "link": "https://www.mintscan.io/rizon/proposals",
    "selector":"div.FeaturedProposals_featuredProposalGrid__3pQ0-",
    "post": "",
    "groups": ""
    },"HIVE": {
    "source": "github-release",
    "link": "https://github.com/openhive-network/hive/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"QKC": {
    "source": "github-repo",
    "link": "https://github.com/QuarkChain/QCEPs/tree/master/QCEP",
    "selector":"",
    "post": "",
    "groups": ""
    },"ZIL": {
    "source": "github-release",
    "link": "https://github.com/Zilliqa/Zilliqa/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"XTZ": {
    "source": "xtz-agora",
    "link": "https://www.tezosagora.org/period/",
    "selector":"div._agoraSelect_95594",
    "post": "",
    "groups": ""
    },"ICX": {
    "source": "icx-forum",
    "link": "https://forum.icon.community/search?expanded=true&q=hard%20fork",
    "selector":"span.topic-title",
    "post": "",
    "groups": ""
    },"VET": {
    "source": "github-release",
    "link": "https://github.com/vechain/thor/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"XEC": {
    "source": "github-release",
    "link": "https://github.com/Bitcoin-ABC/bitcoin-abc/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"SNX": {
    "source": "snx-blog",
    "link": "https://blog.synthetix.io/author/synthetix/",
    "selector":"div ~ h2.post-card-title",
    "post": "",
    "groups": ""
    },"ALGO": {
    "source": "github-release",
    "link": "https://github.com/algorand/go-algorand/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"ONT": {
    "source": "github-release",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"ONG": {
    "source": "github-release",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"IOST": {
    "source": "github-release",
    "link": "https://github.com/iost-official/go-iost/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"QTUM": {
    "source": "github-release",
    "link": "https://github.com/qtumproject/qtum/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"CTK": {
    "source": "github-repo",
    "link": "https://github.com/ShentuChain/mainnet",
    "selector":"",
    "post": "",
    "groups": ""
    },"VELO": {
    "source": "github-release",
    "link": "https://github.com/stellar/stellar-core/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"CENNZ": {
    "source": "github-release",
    "link": "https://github.com/cennznet/cennznet/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"ETC": {
    "source": "xangle",
    "link": "https://xangle.io/insight/disclosure?search=etc&category=network_fork",
    "selector":".bc-insight-list-item-wrapper",
    "post": "",
    "groups": ""
    },"CSPR": {
    "source": "github-wiki",
    "link": "https://github.com/casper-network/casper-node/wiki",
    "selector":"",
    "post": "",
    "groups": ""
    },"REI": {
    "source": "github-release",
    "link": "https://github.com/REI-Network/rei/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"CKB": {
    "source": "github-release",
    "link": "https://github.com/nervosnetwork/ckb/releases/latest",
    "selector":"",
    "post": "",
    "groups": ""
    },"ELF": {
    "source": "github-release",
    "link": "https://github.com/AElfProject/AElf/releases",
    "selector":"",
    "post": "",
    "groups": ""
    },"KCT-7": {
    "source": "github-release",
    "link": "https://github.com/klaytn/klaytn/releases/latest",
    "selector":"",
    "post": "",
    "groups": "HIPS, SSX, TEMCO, WIKEN, OBSR, BORA, NPT, SIX, MBX"
    },"TRC-20": {
    "source": "github-release",
    "link": "https://github.com/tronprotocol/java-tron/releases/latest",
    "selector":"",
    "post": "",
    "groups": "BTT, JST, SUN"
    },"BEP-20": {
    "source": "github-release",
    "link": "https://github.com/bnb-chain/node/releases/latest",
    "selector":"",
    "post": "",
    "groups": "CAKE, XVS, ALT, GMT, C98, SPRT"
    },"ERC-20": {
    "source": "github-release",
    "link": "https://github.com/ethereum/go-ethereum/releases/latest",
    "selector":"",
    "post": "",
    "groups": "OGN, GLM, WOZX, TRV, OCEAN, BOBA"
    }}

if __name__ == "__main__":
    create_coins_db()
    create_xangle_swap_db()
    create_xangle_rebrand_db()
    create_proxy_db()