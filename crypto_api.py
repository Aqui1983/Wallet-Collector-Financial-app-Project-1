import http.client
import requests
import streamlit as st
import json
import pandas as pd



blockchain_list = ["bitcoin", "litecoin", "dogecoin", "ethereum", "xrp"]

blockchain_selection = st.selectbox("Please select the blockchain for your wallet:", blockchain_list)

wallet_address = st.text_input("Please enter your wallet address")

record_df = pd.read_csv('database.csv')

total_assets = []

current_price_url = f"https://api.alternative.me/v2/ticker/{blockchain_selection}/?convert=USD"


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
if st.button("Enter"):
    with requests.Session() as session:
        h = {'Content-Type': 'application/json',
            'X-API-KEY': APIKEY}
        r = session.get(
            f'{BASE}/blockchain-data/{BLOCKCHAIN}/{NETWORK}/addresses/{ADDRESS}/balance', headers=h)
        r.raise_for_status()
        
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        
        amount = float(r.json()['data']['item']['confirmedBalance']['amount'])
        
        coin = r.json()['data']['item']['confirmedBalance']['unit']
        
        record = [wallet_address, {coin:amount}]
        
        price_data = requests.get(current_price_url).json() 
        
        print(json.dumps(price_data, indent=4, sort_keys=True))
        
        crypto_id = price_data

        #price = price_data['data']['{crypto_id}']['quotes']['USD']['price']
        
        #total_assets += amount * price
        
        record_df.loc[len(record_df.index)] = record
        
        record_df.to_csv('database.csv', index = False)
        
        st.write(f"You have {amount} {coin} in this account {crypto_id}")

    
