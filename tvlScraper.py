#'https://defillama.com/docs/api'
#
#protocls
#{'id': '1527', 'name': 'Libero Financial', 'address': 'bsc:0x0DFCb45EAE071B3b846E220560Bbcdd958414d78', 'symbol': 'LIBERO', 'url': 'https://libero.financial/app?lang=en', 'description': 'Libero Autostaking Protocol or LAP, is a new 
# financial protocol that makes staking easier, and gives $LIBERO token holders the highest stable returns in crypto.', 'chain': 'Binance', 'logo': 'https://icons.llama.fi/libero-financial.png', 'audits': '2', 'audit_note': None, 
# 'gecko_id': 'libero-financial', 'cmcId': '17776', 'category': 'Staking', 'chains': ['Binance'], 'oracles': [], 'forkedFrom': [], 'module': 'libero/index.js', 'twitter': 'LiberoFinancial', 'audit_links': 
# ['https://github.com/Rugfreecoins/Smart-Contract-Audits/blob/main/Libero%20Financial%20Token.pdf'], 'listedAt': 1646877651, 'slug': 'libero-financial', 'tvl': 0, 'chainTvls': {'Binance': 0, 'Binance-staking': 7098672.9698173655, 
# 'staking': 7098672.9698173655}, 'change_1h': None, 'change_1d': None, 'change_7d': None, 'staking': 7098672.9698173655, 'fdv': 66945309, 'mcap': 0}]

import requests, json
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dbConnection import getDBURL


def tvlScrape():
    timestamp = datetime.now()
    data = requests.get(f'https://api.llama.fi/protocols')
    print(data)
    id, time, name, url, description, chain, audits, audit_note, cmcId, category, listedAt, tvl, staking, mcap, chain_staking = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for rec in data.json():
        id.append(rec.get('id', None))
        time.append(timestamp)
        name.append(rec.get('name', None))
        url.append(rec.get('url', None))
        description.append(rec.get('description', None))
        chain.append(rec.get('chain', None)) 
        audits.append(rec.get('audits', None)) 
        audit_note.append(rec.get('audit_note', None))
        cmcId.append(rec.get('cmcId', None))
        category.append(rec.get('category', None))
        listedAt.append(rec.get('listedAt', None))
        tvl.append(rec.get('tvl', None))
        staking.append(rec.get('staking', None))
        mcap.append(rec.get('mcap', None))
        chain_staking.append(rec['chainTvls'].get('staking', None))

    protocols = {
        "id" : id,
        "time" : time,
        "name" : name,
        "url" : url,
        "description" : description,
        "chain" : chain,
        "audits" : audits,
        "audit_note" : audit_note,
        "cmcId" : cmcId,
        "category" : category,
        "listedAt" : listedAt,
        "tvl" : tvl,
        "staking" : staking,
        "mcap" : mcap,
        "chain_staking" : chain_staking
    }

    df = pd.DataFrame(protocols, columns = ["id", "time", "name", "url", "description", "chain", "audits", "audit_note", "cmcId", "category", "listedAt", "tvl", "staking", "mcap", "chain_staking"])

    print(df)


    url = getDBURL()
    my_conn=create_engine(url)
    df.to_sql(con=my_conn, name='tvl',if_exists='append', index=False)




