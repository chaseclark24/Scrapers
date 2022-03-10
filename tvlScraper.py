#'https://defillama.com/docs/api'
#
#protocls
#{'id': '1527', 'name': 'Libero Financial', 'address': 'bsc:0x0DFCb45EAE071B3b846E220560Bbcdd958414d78', 'symbol': 'LIBERO', 'url': 'https://libero.financial/app?lang=en', 'description': 'Libero Autostaking Protocol or LAP, is a new 
# financial protocol that makes staking easier, and gives $LIBERO token holders the highest stable returns in crypto.', 'chain': 'Binance', 'logo': 'https://icons.llama.fi/libero-financial.png', 'audits': '2', 'audit_note': None, 
# 'gecko_id': 'libero-financial', 'cmcId': '17776', 'category': 'Staking', 'chains': ['Binance'], 'oracles': [], 'forkedFrom': [], 'module': 'libero/index.js', 'twitter': 'LiberoFinancial', 'audit_links': 
# ['https://github.com/Rugfreecoins/Smart-Contract-Audits/blob/main/Libero%20Financial%20Token.pdf'], 'listedAt': 1646877651, 'slug': 'libero-financial', 'tvl': 0, 'chainTvls': {'Binance': 0, 'Binance-staking': 7098672.9698173655, 
# 'staking': 7098672.9698173655}, 'change_1h': None, 'change_1d': None, 'change_7d': None, 'staking': 7098672.9698173655, 'fdv': 66945309, 'mcap': 0}]

from asyncio.windows_events import NULL
import requests, json
from datetime import datetime
import pandas as pd

timestamp = datetime.now()
data = requests.get(f'https://api.llama.fi/protocols')
id, time, name, url, description, chain, audits, audit_note, cmcId, category, listedAt, tvl, staking, mcap, chain_staking = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

for rec in data.json():
    id.append(rec.get('id', NULL))
    time.append(timestamp)
    name.append(rec.get('name', NULL))
    url.append(rec.get('url', NULL))
    description.append(rec.get('description', NULL))
    chain.append(rec.get('chain', NULL)) 
    audits.append(rec.get('audits', NULL)) 
    audit_note.append(rec.get('audit_note', NULL))
    cmcId.append(rec.get('cmcId', NULL))
    category.append(rec.get('category', NULL))
    listedAt.append(rec.get('listedAt', NULL))
    tvl.append(rec.get('tvl', NULL))
    staking.append(rec.get('staking', NULL))
    mcap.append(rec.get('mcap', NULL))
    chain_staking.append(rec['chainTvls'].get('staking', NULL))

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