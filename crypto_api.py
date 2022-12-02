import http.client
import requests
import streamlit as st
import json
import pandas as pd


# our lists for various functions such as populating coins, addresses, current price of coin and record keeping of accounts entered
blockchain_list = ["bitcoin", "dogecoin", "ethereum", "xrp"]

blockchain_selection = st.selectbox("Please select the blockchain for your wallet:", blockchain_list)

wallet_address = st.text_input("Please enter your wallet address")

record_df = pd.read_csv('database.csv')

total_value_asset = None

current_price_url = f"https://api.alternative.me/v2/ticker/{blockchain_selection}/?convert=USD"

crypto_id = ""

#records = {}

# Dummy Addresses
    # BTC = n4VQ5YdHf7hLQ2gWQYYrcxoE5B7nWuDFNF
    # ETH = 0x00000000219ab540356cbb839cbe05303d7705fa
    # XRP = rBiu2po3VWmD9N7XBMmGRpDe7qLwFTegyW
    # DOGE = nbMFaHF9pjNoohS4fD1jefKBgDnETK9uPu

# IF statement for network

if blockchain_selection == "ethereum":
    network_selection = 'goerli'
    crypto_id = '1027'
elif blockchain_selection == "bitcoin":
    network_selection = 'testnet'
    crypto_id = '1'
elif blockchain_selection == "dogecoin":
    network_selection = 'testnet'
    crypto_id = '74'
elif blockchain_selection == "xrp":
    network_selection = 'testnet'
    crypto_id = '52'
else:
    st.error("You have not chosen a compatible network")


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
        
        print(json.dumps(price_data, indent=4))

        price = price_data['data'][crypto_id]['quotes']['USD']['price']

        total_value_asset = amount * price
        
        record_df.loc[len(record_df.index)] = record
        
        record_df.to_csv('database.csv', index = False)
        
        st.write(f"You have {amount} {coin} in this account. Its total current value is {round(total_value_asset,2)}")

    
