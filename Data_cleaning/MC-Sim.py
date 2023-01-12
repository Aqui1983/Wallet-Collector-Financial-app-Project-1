import http.client
import yfinance as yf
import requests
import streamlit as st
import json
import pandas as pd 
import plotly
import plotly.graph_objects as go
import plotly.express as px 
import plotly.io as pio
import numpy as np
import functools
import matplotlib.pyplot as plt
import datetime as dt
import base64
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from plotly.subplots import make_subplots
from PIL import Image
from urllib.request import urlopen
from project.MCForecastTools_copy import MCSimulation
from bs4 import BeautifulSoup 

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
    # DOGE = nbMFaHF9pjNoohS4fD1jefKBgDnETK9uPu , ndptgeN9zESnZgc84bXFshFhyxx3PzKtpY , niPMVR1mhcyL63BeXaBwJiiKCccFwV7xHh

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


# API KEY and making main wallet aggregater function
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
        
        amount = float(r.json()['data']['item']['confirmedBalance']['amount'])
        
        coin = r.json()['data']['item']['confirmedBalance']['unit']
                
        price_data = requests.get(GetPrice(token)).json() 
        
        print(json.dumps(price_data, indent=4))

        price = price_data['data'][crypto_id]['quotes']['USD']['price']

        last_price = price_data['data'][crypto_id]['quotes']['USD']['price']

        total_value_asset = amount * round(price,2)

        record = [wallet_address, coin, amount, price, total_value_asset]
        
        record_df.loc[len(record_df.index)] = record
        
        record_df.to_csv('database.csv', index = False)

        record_df.drop_duplicates(subset='Address', keep='last', inplace=True)
       
    
        record_df.drop_duplicates(keep='last', inplace=True)
        
        st.write(record_df.keys())
        
        assets_total = record_df[record_df.keys()[-1]].sum()

st.subheader("Coin percentage of total value")
st.write("Formula working brainstorm")

record_df.sum(record_df.keys()[1] == 'BTC')

st.write(record_df)
    
#print(record_df.loc['r4']['Duration'])
#print(record_df.loc['r4'][2])


#BTC_pct = record_df[record_df.keys()[1] == 'BTC']


#st.write(BTC_pct).sum()
    
    
    
record = {

'Address': [record_df.keys()[0]],
'Coins': [record_df.keys()[1]],
'Amount': [[record_df.keys()[2]]],
'Last Price': [[record_df.keys()[3]]],
'Total Value': [[record_df.keys()[4]]]
}
    # MARC TESTING CODE
        #st.dataframe(assets_total)
#st.write('The total value in your Wallet Collection is:')
        
total_amount_ml = record_df[record_df.keys()[-1]].sum()

total_amount_ml = round(total_amount_ml,2)

#st.write(total_amount_ml)
                
#percentage of total per coin


# btc_value = record_df.query('Coins'=="ETH")

#btc_value = record_df[record_df.keys()[1].values == 'ETH']

# st.write(btc_value)

# record_df[record_df.keys()[1] == 'BTC']

#st.write('The total value of Bitcoin in your Wallet Collection is:')
#st.write(btc_value)
        
# create a dataframe


#st.write("Given Dataframe :\n", record_df) 

# selecting rows based on condition
BTC_df = record_df[record_df[record_df.keys()[1]] == 'BTC']
ETH_df = record_df[record_df[record_df.keys()[1]] == 'ETH']
XRP_df = record_df[record_df[record_df.keys()[1]] == 'XRP']
DOGE_df = record_df[record_df[record_df.keys()[1]] == 'DOGE']


#can comment out or delete
#st.write('\nResult dataframe :\n', BTC_df)
#st.write('\nResult dataframe :\n', ETH_df)
#st.write('\nResult dataframe :\n', DOGE_df)


BTC_total = BTC_df.sum()
BTC_total_value = BTC_total[BTC_total.keys()[-1]].sum()
st.write('\nBitcoin Wallet Value:\n', BTC_total_value)

btc_pct = BTC_total_value / total_amount_ml
st.write('\Bitcoin % of Portfolio :\n', btc_pct)

ETH_total = ETH_df.sum()
ETH_total_value = ETH_total[ETH_total.keys()[-1]].sum()
st.write('\nEthereum Wallet Value :\n', ETH_total_value)

eth_pct = ETH_total_value / total_amount_ml
st.write('\Ethereum % of Portfolio :\n', eth_pct)


XRP_total = XRP_df.sum()
XRP_total_value = XRP_total[XRP_total.keys()[-1]].sum()
st.write('\nRipple Wallet Value :\n', XRP_total_value)

xrp_pct = XRP_total_value / total_amount_ml
st.write('\Ripple % of Portfolio :\n', xrp_pct)


DOGE_total = DOGE_df.sum()
DOGE_total_value = DOGE_total[DOGE_total.keys()[-1]].sum()
st.write('\nDogecoin Wallet Value :\n', DOGE_total_value)

doge_pct = DOGE_total_value / total_amount_ml
st.write('\nDogecoin % of Portfolio :\n', doge_pct)

coin_weights = (btc_pct, eth_pct, xrp_pct, doge_pct)

#st.write(coin_weights) 


        
        
# Monte Carlo Section

#mc_years_list = ['1', '3', '5', '10']

#st.write(mc_years_list)

years = st.slider('How many years into the future do you want to see?', min_value=1, max_value=10, step=1)

Bitcoin = 'BTC-USD'
Ethereum = 'ETH-USD'
Ripple = 'XRP-USD'
Dogecoin = 'DOGE-USD'

# Download Stock Data

st.write("# Download Stock Data")

BTC = yf.download(Bitcoin, period="max", interval="1d")
ETH = yf.download(Ethereum, period="max", interval="1d")
XRP = yf.download(Ripple, period="max", interval="1d")
DOG = yf.download(Dogecoin, period="max", interval="1d")

# Starting to clean dataframes and get them ready to concact
All_coins_hist_df = pd.concat([BTC, ETH, XRP, DOG],axis=1, keys=['BTC', 'ETH', 'XRP', 'DOG'])
All_coins_hist_df = All_coins_hist_df.dropna()

# display(All_coins_hist_df.head())
#display(All_coins_hist_df.tail())


Monte_carlo_sim = MCSimulation(
    portfolio_data = All_coins_hist_df,
    weights = [btc_pct, eth_pct, xrp_pct, doge_pct],
    num_simulation = 500,
    num_trading_days = 365 * years
)
daily_returns_df = Monte_carlo_sim.calc_cumulative_return()
#st.write(daily_returns_df)

line_plot_MC_sim = Monte_carlo_sim.plot_simulation()
plt.savefig('image1.png')
img=plt.imread('image1.png')
st.image(img)

tbl_5yr = Monte_carlo_sim.summarize_cumulative_return()

st.write(tbl_5yr)