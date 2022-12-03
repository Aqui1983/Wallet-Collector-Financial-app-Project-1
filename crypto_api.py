import http.client
import requests
import streamlit as st
import json
import pandas as pd
import plotly.express as px 

# our lists for various functions such as populating coins, addresses, current price of coin and record keeping of accounts entered
blockchain_list = ["bitcoin", "dogecoin", "ethereum", "xrp"]

blockchain_selection = st.sidebar.selectbox("Please select the blockchain for your wallet:", blockchain_list)

wallet_address = st.sidebar.text_input("Please enter your wallet address")

record_df = pd.read_csv('database.csv')

total_value_asset = None

crypto_id = ""

asset_weights = ""

token = None

def GetPrice(token):
    price = f"https://api.alternative.me/v2/ticker/{token}/?convert=USD"
    return(price)

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
    token = 'ethereum'
elif blockchain_selection == "bitcoin":
    network_selection = 'testnet'
    crypto_id = '1'
    token = 'bitcoin'
elif blockchain_selection == "dogecoin":
    network_selection = 'testnet'
    crypto_id = '74'
    token = 'dogecoin'
elif blockchain_selection == "xrp":
    network_selection = 'testnet'
    crypto_id = '52'
    token = 'ripple'
else:
    st.error("You have not chosen a compatible network")


# API KEY
APIKEY = '792ab6c22be07b385449661875579f1316e11ad9' # <-----
BASE = 'https://rest.cryptoapis.io'
BLOCKCHAIN = blockchain_selection
NETWORK = network_selection #################
ADDRESS = wallet_address
if st.sidebar.button("Enter"):
    with requests.Session() as session:
        h = {'Content-Type': 'application/json',
            'X-API-KEY': APIKEY}
        r = session.get(
            f'{BASE}/blockchain-data/{BLOCKCHAIN}/{NETWORK}/addresses/{ADDRESS}/balance', headers=h)
        r.raise_for_status()
        print(json.dumps(r.json(), indent=4, sort_keys=True))
        # This code deals with type of coins and amount of coins being pulled from the CryptoAPI.io API
        amount = float(r.json()['data']['item']['confirmedBalance']['amount'])
        
        coin = r.json()['data']['item']['confirmedBalance']['unit']
        # This code deals with the current price on the coins being pulled from the alternative me API        
        price_data = requests.get(GetPrice(token)).json() 
        
        print(json.dumps(price_data, indent=4))

        price = price_data['data'][crypto_id]['quotes']['USD']['price']

        last_price = price_data['data'][crypto_id]['quotes']['USD']['price']

        total_value_asset = amount * round(price,2)
        # This code makes the columns for the csv and loads the dataframe, made by the address entries from the streamlit dashboard, into the csv.
        record = [wallet_address, coin, amount, price, total_value_asset]
        
        record_df.loc[len(record_df.index)] = record
        
        record_df.to_csv('database.csv', index = False)

        record_df.drop_duplicates(keep='last', inplace=True)

        
        st.write(record_df.keys())
        
        assets_total = record_df[record_df.keys()[-1]].sum()
        
        st.write(assets_total)
        st.subheader(f"You have {amount} {coin} in this account. Its total current value is ${round(total_value_asset,2)}")

        st.header('Wallet Collection')
        st.dataframe(record_df)
        st.subheader('The total value in your Wallet Collection is {assets_total}')

#Annual_Income = st.sidebar.text_input("Please enter your Annual Income")
#if st.button("Enter"):

    

# This dataframe has 244 lines, but 4 distinct values for `day`
#df = px.data.tips()
#fig = px.pie(df, values='tip', names='day')
#fig.show()
