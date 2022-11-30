import http.client
import requests
import streamlit as st
import json



blockchain_list = ["bitcoin", "litecoin", "dogecoin", "ethereum", "xrp"]

blockchain_selection = st.selectbox("Please select the blockchain for your wallet:", blockchain_list)

wallet_address = st.text_input("Please enter your wallet address")

# Dummy Addresses
    # BTC = n4VQ5YdHf7hLQ2gWQYYrcxoE5B7nWuDFNF
    # ETH = 0x00000000219ab540356cbb839cbe05303d7705fa
    # XRP = rBiu2po3VWmD9N7XBMmGRpDe7qLwFTegyW
    # DOGE = nbMFaHF9pjNoohS4fD1jefKBgDnETK9uPu

# IF statement for network

if blockchain_selection == "ethereum":
    network_selection = 'goerli'
else:
    network_selection = 'testnet'

# API KEY

APIKEY = '792ab6c22be07b385449661875579f1316e11ad9' # <-----
BASE = 'https://rest.cryptoapis.io'
BLOCKCHAIN = blockchain_selection
NETWORK = network_selection #################
ADDRESS = wallet_address
with requests.Session() as session:
    h = {'Content-Type': 'application/json',
         'X-API-KEY': APIKEY}
    r = session.get(
        f'{BASE}/blockchain-data/{BLOCKCHAIN}/{NETWORK}/addresses/{ADDRESS}/balance', headers=h)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=4, sort_keys=True))
    
    