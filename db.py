import sqlite3
import os
import json

def create_coins_db():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()

    # Create table
    cur.execute("CREATE TABLE coins (name PRIMARY KEY, source NOT NULL, link NOT NULL, post, groups)")
    con.commit()

    # insert first values
    query = "INSERT INTO coins VALUES (?, ?, ?, ?, ?)"
    for coin in coins.items():
        params = list((coin[0], coin[1]["source"], coin[1]["link"], coin[1]["post"], coin[1]["groups"]))
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
def insert_coin(coins):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "INSERT INTO coins VALUES (?, ?, ?, ?, ?)"

    for coin in coins.items():
        params = list((coin[0], coin[1]["source"], coin[1]["link"], coin[1]["post"], coin[1]["groups"]))
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
        "source": item[1],
        "link": item[2],
        "post": item[3],
        "groups": item[4]}
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
            "post": i[3],
            "groups": i[4]})
        return res
    except:
        return None
def update_post(post, coin):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET post = ? WHERE name = ?"
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

coins = {
    "META": {
    "source": "brunch",
    "link": "https://brunch.co.kr/magazine/metadium-info",
    "post": "",
    "groups": ""
    },
    "EGLD": {
    "source": "github-release",
    "link": "https://github.com/ElrondNetwork/elrond-go/releases/latest",
    "post": "",
    "groups": ""
    },
    "THETA": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "post": "",
    "groups": ""
    },
    "TFUEL": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "post": "",
    "groups": ""
    },
    "TDROP": {
    "source": "github-release",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "post": "",
    "groups": ""
    },
    "CTXC": {
    "source": "github-release",
    "link": "https://github.com/CortexFoundation/CortexTheseus/releases/latest",
    "post": "",
    "groups": ""
    },
    "MEDI": {
    "source": "github-repo",
    "link": "https://github.com/medibloc/panacea-governance/tree/main/proposals",
    "post": "",
    "groups": ""
    },
    "XYM": {
    "source": "github-release",
    "link": "https://github.com/symbol/symbol/releases/latest",
    "post": "",
    "groups": ""
    },
    "ATOLO": {
    "source": "mintscan",
    "link": "https://www.mintscan.io/rizon/proposals",
    "post": "",
    "groups": ""
    },"HIVE": {
    "source": "github-release",
    "link": "https://github.com/openhive-network/hive/releases/latest",
    "post": "",
    "groups": ""
    },"QKC": {
    "source": "github-repo",
    "link": "https://github.com/QuarkChain/QCEPs/tree/master/QCEP",
    "post": "",
    "groups": ""
    },"ZIL": {
    "source": "github-release",
    "link": "https://github.com/Zilliqa/Zilliqa/releases/latest",
    "post": "",
    "groups": ""
    },"XTZ": {
    "source": "xtz-agora",
    "link": "https://www.tezosagora.org/period/86",
    "post": "",
    "groups": ""
    },"ICX": {
    "source": "icx-forum",
    "link": "https://forum.icon.community/search?expanded=true&q=hard%20fork",
    "post": "",
    "groups": ""
    },"VET": {
    "source": "github-release",
    "link": "https://github.com/vechain/thor/releases/latest",
    "post": "",
    "groups": ""
    },"XEC": {
    "source": "xec-release",
    "link": "https://www.bitcoinabc.org/releases/latest/",
    "post": "",
    "groups": ""
    },"SNX": {
    "source": "snx-blog",
    "link": "https://blog.synthetix.io/author/synthetix/",
    "post": "",
    "groups": ""
    },"ALGO": {
    "source": "github-release",
    "link": "https://github.com/algorand/go-algorand/releases/latest",
    "post": "",
    "groups": ""
    },"ONT": {
    "source": "github-release",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "post": "",
    "groups": ""
    },"ONG": {
    "source": "github-release",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "post": "",
    "groups": ""
    },"IOST": {
    "source": "github-release",
    "link": "https://github.com/iost-official/go-iost/releases/latest",
    "post": "",
    "groups": ""
    },"QTUM": {
    "source": "github-release",
    "link": "https://github.com/qtumproject/qtum/releases/latest",
    "post": "",
    "groups": ""
    },"CTK": {
    "source": "github-repo",
    "link": "https://github.com/ShentuChain/mainnet",
    "post": "",
    "groups": ""
    },"VELO": {
    "source": "github-release",
    "link": "https://github.com/stellar/stellar-core/releases/latest",
    "post": "",
    "groups": ""
    },"CENNZ": {
    "source": "github-release",
    "link": "https://github.com/cennznet/cennznet/releases/latest",
    "post": "",
    "groups": ""
    },"ETC": {
    "source": "xangle",
    "link": "https://xangle.io/insight/disclosure?search=etc&category=network_fork",
    "post": "",
    "groups": ""
    },"CSPR": {
    "source": "detect-page-change",
    "link": "https://github.com/casper-network/casper-node/wiki/Upgrade-to-Casper-node-v1.4.9",
    "post": "",
    "groups": ""
    },"REI": {
    "source": "github-release",
    "link": "https://github.com/REI-Network/rei/releases/latest",
    "post": "",
    "groups": ""
    },"CKB": {
    "source": "github-release",
    "link": "https://github.com/nervosnetwork/ckb/releases/latest",
    "post": "",
    "groups": ""
    },"KCT-7": {
    "source": "github-release",
    "link": "https://github.com/klaytn/klaytn/releases/latest",
    "post": "",
    "groups": "HIPS, SSX, TEMCO, WIKEN, OBSR, BORA, NPT, SIX, MBX"
    },"TRC-20": {
    "source": "github-release",
    "link": "https://github.com/tronprotocol/java-tron/releases/latest",
    "post": "",
    "groups": "BTT, JST, SUN"
    },"BEP-20": {
    "source": "github-release",
    "link": "https://github.com/bnb-chain/node/releases/latest",
    "post": "",
    "groups": "CAKE, XVS, ALT, GMT, C98, SPRT"
    },"ERC-20": {
    "source": "github-release",
    "link": "https://github.com/ethereum/go-ethereum/releases/latest",
    "post": "",
    "groups": "OGN, GLM, WOZX, TRV, OCEAN, BOBA"
    }}