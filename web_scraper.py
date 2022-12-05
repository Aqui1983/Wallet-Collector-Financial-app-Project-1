#making a web scraper for crypto price data
#imports
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time


#Page layout, dividing into 3 columns
col1 = st.sidebar
col2, col3 = st.columns((2,1))

@st.cache
def scrape_data():
    cmc = requests.get('https://www.coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']

    for i in listings[1:]:
        coins[i[-4]] = i[-4]
    
    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h= []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []
    for i in listings[1:]:
        coin_name.append(i[14])
        coin_symbol.append(i[-4])
        price.append(i[64])
        percent_change_1h.append(i[58])
        percent_change_24h.append(i[59])
        percent_change_7d.append(i[62])
        market_cap.append(i[55])
        volume_24h.append(i[67])
    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df


df = scrape_data()



# Sidebar crptocurrency selector

sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Crypotocurrency', sorted_coin, sorted_coin)

# Filtering the data
df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin))]

# Sidebar amount of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

# Sidebar percent changetimeframe selector
percent_timeframe = col1.selectbox('Percent change time frame', 
                                    ['7d', '24h', '1h'])
percent_dict = {'7d':'percentChange7d','24h':'percentChange24h','1h':'percentChange1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# SIdebar Sort value selector Y/N
sort_values = col1.selectbox('Sort values?', ['Yes','No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

# Download data to CSV
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)


#Bar plot for percentage change in price
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# If statements for Bar plot time frame
col3.subheader('Barplot of % Price Change')

if percent_timeframe =='7d':
    if sort_values =='Yes':
        df_change =df_change.sort_values(by=['percent_change_7d'])
    col3.write('*7 days period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe =='24h':
    if sort_values =='Yes':
        df_change =df_change.sort_values(by=['percent_change_24h'])
    col3.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values =='Yes':
        df_change =df_change.sort_values(by=['percent_change_1h'])
    col3.write('*1 hour period')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)



