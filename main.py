import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
from urllib.request import urlopen



#titles

st.title("Crypto Currency Daily Prices")
st.header("Main Dashboard")
st.subheader("you can add more crypto in code")

Bitcoin = 'BTC-USD'
Ethereum = 'ETH-USD'
Ripple = 'XRP-USD'
Bitcoincash = 'BCH-USD'
Cardano = 'ADA-USD'

 
 
 # Download Stock Data

st.write("# Download Stock Data")
address=st.text_input("Please enter wallet address to be evaluated")
BTC = yf.download(Bitcoin, period="max", interval="1d")
ETH = yf.download(Ethereum, period="max", interval="1d")
XRP = yf.download(Ripple, period="max", interval="1d")
BCH = yf.download(Bitcoincash, period="max", interval="1d")
ADA = yf.download(Cardano, period="max", interval="1d")

BTC
ETH
XRP
BCH
ADA


# Ticker Data

BTC_Data =  yf.Ticker(Bitcoin)
ETH_Data =  yf.Ticker(Ethereum)
XRP_Data =  yf.Ticker(Ripple)
BCH_Data =  yf.Ticker(Bitcoincash)
ADA_Data = yf.Ticker(Cardano)


# Stock - Info

st.write("# Stock - Info")
btc_info = BTC_Data.info
eth_info = ETH_Data.info
xrp_info = XRP_Data.info
bch_info = BCH_Data.info
ada_info = ADA_Data.info

btc_info.keys()
eth_info.keys()
xrp_info.keys()
bch_info.keys()
ada_info.keys()


# Stock - Histories

st.write("# Stock - History")
btc_hist = BTC_Data.history(period="max")
eth_hist = ETH_Data.history(period="max")
xrp_hist = XRP_Data.history(period="max")
bch_hist = BCH_Data.history(period="max")
ada_hist = ADA_Data.history(period="max")


btc_hist
eth_hist
xrp_hist
bch_hist
ada_hist























st.write("BITCOIN ($)")


 
 