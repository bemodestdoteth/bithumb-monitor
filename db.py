import sqlite3
import os
import json

def create_coins_db(coins):
    if not(os.path.isfile('coins.db')):
        con = sqlite3.connect('coins.db')
        cur = con.cursor()

        # Create table
        cur.execute("CREATE TABLE coins (name PRIMARY KEY, source NOT NULL, link NOT NULL, posts)")
        con.commit()

        # insert first values
        insert_coin(coins)
def insert_coin(coins):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "INSERT INTO coins VALUES (?, ?, ?, ?)"

    for coin in coins.items():
        params = list((coin[0], coin[1]["source"], coin[1]["link"], coin[1]["posts"]))
        cur.execute(query, params)
    con.commit()
def get_coin(coin):
    # Import DB to get coin information
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    # params = os.path.basename(os.path.dirname(__file__))
    query = "SELECT * FROM coins WHERE name = ?"
    item = cur.execute(query, (coin,)).fetchone()
    return {
        "name": item[0],
        "link": item[1],
        "posts": item[2],
        "group": item[3]}
def change_post(post, coin):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET posts = ? WHERE name = ?"
    cur.execute(query, (json.dumps(post), coin))
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
    "source": "brunch",
    "link": "https://brunch.co.kr/magazine/metadium-info",
    "posts": "",
    "group": ""
    },
    "EGLD": {
    "source": "github-release",
    "link": "https://github.com/ElrondNetwork/elrond-go/releases/latest",
    "posts": "",
    "group": ""
    },
    "THETA": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "posts": "",
    "group": ""
    },
    "TFUEL": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "posts": "",
    "group": ""
    },
    "TDROP": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "posts": "",
    "group": ""
    },
    "CTXC": {
    "source": "github-release",
    "link": "https://github.com/CortexFoundation/CortexTheseus/releases/latest",
    "posts": "",
    "group": ""
    },
    "MEDI": {
    "source": "github-repo",
    "link": "https://github.com/CortexFoundation/CortexTheseus/releases/latest",
    "posts": "",
    "group": ""
    },
    "XYM": {
    "source": "github-release",
    "link": "https://github.com/symbol/symbol/releases/latest",
    "posts": "",
    "group": ""
    },
    "ATOLO": {
    "source": "mintscan",
    "link": "https://www.mintscan.io/rizon/proposals",
    "posts": "",
    "group": ""
    },"HIVE": {
    "source": "github-release",
    "link": "https://github.com/openhive-network/hive/releases/latest",
    "posts": "",
    "group": ""
    },"QKC": {
    "source": "github-repo",
    "link": "https://github.com/QuarkChain/QCEPs/tree/master/QCEP",
    "posts": "",
    "group": ""
    },"ZIL": {
    "source": "github-release",
    "link": "https://github.com/Zilliqa/Zilliqa/releases/latest",
    "posts": "",
    "group": ""
    },"XTZ": {
    "source": "xtz-agora",
    "link": "https://www.tezosagora.org/period/86",
    "posts": "",
    "group": ""
    },"ICX": {
    "source": "icx-forum",
    "link": "https://forum.icon.community/search?expanded=true&q=hard%20fork",
    "posts": "",
    "group": ""
    },"VET": {
    "source": "github-release",
    "link": "https://github.com/vechain/thor/releases/latest",
    "posts": "",
    "group": ""
    },"XEC": {
    "source": "xec-release",
    "link": "https://www.bitcoinabc.org/releases/latest/",
    "posts": "",
    "group": ""
    },"SNX": {
    "source": "snx-blog",
    "link": "https://blog.synthetix.io/author/synthetix/",
    "posts": "",
    "group": ""
    },"ALGO": {
    "source": "github-release",
    "link": "https://github.com/algorand/go-algorand/releases/latest",
    "posts": "",
    "group": ""
    },"ONT": {
    "source": "github-release",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "posts": "",
    "group": ""
    },"ONG": {
    "source": "github-release",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "posts": "",
    "group": ""
    },"IOST": {
    "source": "github-release",
    "link": "https://github.com/iost-official/go-iost/releases/latest",
    "posts": "",
    "group": ""
    },"QTUM": {
    "source": "github-release",
    "link": "https://github.com/qtumproject/qtum/releases/latest",
    "posts": "",
    "group": ""
    },"CTK": {
    "source": "github-repo",
    "link": "https://github.com/ShentuChain/mainnet",
    "posts": "",
    "group": ""
    },"VELO": {
    "source": "github-release",
    "link": "https://github.com/stellar/stellar-core/releases/latest",
    "posts": "",
    "group": ""
    },"CENNZ": {
    "source": "github-release",
    "link": "https://github.com/cennznet/cennznet/releases/latest",
    "posts": "",
    "group": ""
    },"ETC": {
    "source": "xangle",
    "link": "https://xangle.io/insight/disclosure?search=etc&category=network_fork",
    "posts": "",
    "group": ""
    },"CSPR": {
    "source": "detect-page-change",
    "link": "https://github.com/casper-network/casper-node/wiki/Upgrade-to-Casper-node-v1.4.9",
    "posts": "",
    "group": ""
    },"REI": {
    "source": "github-release",
    "link": "https://github.com/REI-Network/rei/releases/latest",
    "posts": "",
    "group": ""
    },"CKB": {
    "source": "github-release",
    "link": "https://github.com/nervosnetwork/ckb/releases/latest",
    "posts": "",
    "group": ""
    },"KCT-7": {
    "source": "github-release",
    "link": "https://github.com/klaytn/klaytn/releases/latest",
    "posts": "",
    "group": "HIPS, SSX, TEMCO, WIKEN, OBSR, BORA, NPT, SIX, MBX"
    },"TRC-20": {
    "source": "github-release",
    "link": "https://github.com/tronprotocol/java-tron/releases/latest",
    "posts": "",
    "group": "BTT, JST, SUN"
    },"BEP-20": {
    "source": "github-release",
    "link": "https://github.com/bnb-chain/node/releases/latest",
    "posts": "",
    "group": "CAKE, XVS, ALT, GMT, C98, SPRT"
    },"ERC-20": {
    "source": "github-release",
    "link": "https://github.com/ethereum/go-ethereum/releases/latest",
    "posts": "",
    "group": "OGN, GLM, WOZX, TRV, OCEAN, BOBA"
    }}

print(len(coins.keys()))
#create_coins_db(coins)

con = sqlite3.connect('coins.db')
cur = con.cursor()
cur.execute("UPDATE coins SET link = ? WHERE name = ?", (coins["EGLD"]["link"], "EGLD"))
con.commit()