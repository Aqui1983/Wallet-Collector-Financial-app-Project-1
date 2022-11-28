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


# Stock - actions

st.write("# Stock - actions")
btc_actions = BTC_Data.actions
eth_actions = ETH_Data.actions
xrp_actions = XRP_Data.actions
bch_actions = BCH_Data.actions
ada_actions = ADA_Data.actions

btc_actions
eth_actions
xrp_actions
bch_actions
ada_actions


# Stock - dividends

st.write("# Stock - dividends")
btc_dividends = BTC_Data.dividends
eth_dividends = ETH_Data.dividends
xrp_dividends = XRP_Data.dividends
bch_dividends = BCH_Data.dividends
ada_dividends = ADA_Data.dividends

btc_dividends
eth_dividends
xrp_dividends
bch_dividends
ada_dividends


# Stock - splits

st.write("# Stock - splits")
btc_splits = BTC_Data.splits
eth_splits = ETH_Data.splits
xrp_splits = XRP_Data.splits
bch_splits = BCH_Data.splits
ada_splits = ADA_Data.splits

btc_splits
eth_splits
xrp_splits
bch_splits
ada_splits


# Stock - financials

st.write("# Stock - financials")
btc_financials = BTC_Data.financials
eth_financials = ETH_Data.financials
xrp_financials = XRP_Data.financials
bch_financials = BCH_Data.financials
ada_financials = ADA_Data.financials

btc_financials
eth_financials
xrp_financials
bch_financials
ada_financials

# Stock - quarterly_financials

st.write("# Stock - quarterly_financials")
btc_quarterly_financials = BTC_Data.quarterly_financials
eth_quarterly_financials = ETH_Data.quarterly_financials
xrp_quarterly_financials = XRP_Data.quarterly_financials
bch_quarterly_financials = BCH_Data.quarterly_financials
ada_quarterly_financials = ADA_Data.quarterly_financials

btc_quarterly_financials
eth_quarterly_financials
xrp_quarterly_financials
bch_quarterly_financials
ada_quarterly_financials


# Stock - major_holders

st.write("# Stock - major_holders")
btc_major_holders = BTC_Data.major_holders
eth_major_holders = ETH_Data.major_holders
xrp_major_holders = XRP_Data.major_holders
bch_major_holders = BCH_Data.major_holders
ada_major_holders = ADA_Data.major_holders

btc_major_holders
eth_major_holders
xrp_major_holders
bch_major_holders
ada_major_holders



# Stock - institutional_holders

st.write("# Stock - institutional_holders")
btc_ih = BTC_Data.institutional_holders
eth_ih = ETH_Data.institutional_holders
xrp_ih = XRP_Data.institutional_holders
bch_ih = BCH_Data.institutional_holders
ada_ih = ADA_Data.institutional_holders

btc_ih
eth_ih
xrp_ih
bch_ih
ada_ih


# Stock - balance_sheet

st.write("# Stock - balance_sheet")
btc_bs = BTC_Data.balance_sheet
eth_bs = ETH_Data.balance_sheet
xrp_bs = XRP_Data.balance_sheet
bch_bs = BCH_Data.balance_sheet
ada_bs = ADA_Data.balance_sheet

btc_bs
eth_bs
xrp_bs
bch_bs
ada_bs


# Stock - quarterly_balance_sheet

st.write("# Stock - quarterly_balance_sheet")
btc_qbs = BTC_Data.quarterly_balance_sheet
eth_qbs = ETH_Data.quarterly_balance_sheet
xrp_qbs = XRP_Data.quarterly_balance_sheet
bch_qbs = BCH_Data.quarterly_balance_sheet
ada_qbs = ADA_Data.quarterly_balance_sheet

btc_qbs
eth_qbs
xrp_qbs
bch_qbs
ada_qbs


# Stock - cashflow

st.write("# Stock - cashflow")
btc_cashflow = BTC_Data.cashflow
eth_cashflow = ETH_Data.cashflow
xrp_cashflow = XRP_Data.cashflow
bch_cashflow = BCH_Data.cashflow
ada_cashflow = ADA_Data.cashflow

btc_cashflow
eth_cashflow
xrp_cashflow
bch_cashflow
ada_cashflow

# Stock - earnings

st.write("# Stock - earnings")
btc_earnings = BTC_Data.earnings
eth_earnings = ETH_Data.earnings
xrp_earnings = XRP_Data.earnings
bch_earnings = BCH_Data.earnings
ada_earnings = ADA_Data.earnings

btc_earnings
eth_earnings
xrp_earnings
bch_earnings
ada_earnings
















st.write("BITCOIN ($)")
imageBTC = Image.open(urlopen('https://s2.coinmarketcap.com/static/img/coins/64x64/1.png'))

# Display Image

st.image(imageBTC)
  
# Display dataframe
 
st.table(BTC)
 
st.bar_chart(BTCHis.Close)
 
 