import yfinance as yf
import pandas as pd
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

 

#access to Data

BTC_Data =  yf.Ticker(Bitcoin)
ETH_Data =  yf.Ticker(Ethereum)
XRP_Data =  yf.Ticker(Ripple)
BCH_Data =  yf.Ticker(Bitcoincash)
ADA_Data = yf.Ticker(Cardano)

BTCHis = BTC_Data.history(period="max")
ETHHis = ETH_Data.history(period="max")
XRPHis = XRP_Data.history(period="max")
BCHHis = BCH_Data.history(period="max")
ADAHis = ADA_Data.history(period="max")


BTC = yf.download(Bitcoin, start="2022-11-20", end="2022-11-20")
ETH = yf.download(Ethereum, start="2022-11-20", end="2022-11-20")
XRP = yf.download(Ripple, start="2022-11-20", end="2022-11-20")
BCH = yf.download(Bitcoincash, start="2022-11-20", end="2022-11-20")
ADA = yf.download(Cardano, start="2022-11-20", end="2022-11-20")



st.write("BITCOIN ($)")
imageBTC = Image.open(urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'))

# Display Image

st.image(imageBTC)
  
# Display dataframe
 
st.table(BTC)
 
st.bar_chart(BTCHis.Close)
 
 
 
 # Messing Around


st.subheader("# Just Messing Around")

BTC_Data.info
ETH_Data.info
XRP_Data.info
BCH_Data.info
ADA_Data.info
 


BTC_Data.actions 

BTC_Data.recommendations