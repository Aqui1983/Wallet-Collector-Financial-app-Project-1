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
from MCForecastTools_copy import MCSimulation
from bs4 import BeautifulSoup 

#initial functions that need to load before anything else (1)

#Page layout, title, dividing into 3 columns with an expander bar

st.set_page_config(layout="wide")
st.title('Wallet Collector')
st.markdown("""
This app can aggregate all of your wallets in one convenient place with unique insights and the ability to look into the future ;)

""")
expander_bar = st.expander('Price change of top 100 coins DataFrames and coin selector')
col1 = st.sidebar
col2, col3, col4 = st.columns((2,2,1))

#Web Scraper functions to have it display immediately
@st.cache
def scrape_data():
    cmc = requests.get('https://www.coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')
    #cleaning the data to be used for the pct_change bar plot
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']

    #finding the coin names in the data and making the lists for each column
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
    #concacting the dataframe that will be used for display
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
#initial functions that need to load before anything else (2)
#Getting historical price data for candlestick plot
BTC = yf.download('BTC-USD')
BTC.to_csv('BTC.csv')
ETH = yf.download('ETH-USD')
ETH.to_csv('ETH.csv')
XRP = yf.download('XRP-USD')
XRP.to_csv('XRP.csv')
DOGE = yf.download('DOGE-USD')
DOGE.to_csv('DOGE.csv')

#defining candlestick plot function
def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int,
        ticker: str
):
    
    #Create the candlestick chart with two moving avgs + a plot of the volume
    #Parameters
    #----------
    #df : pd.DataFrame
        #The price dataframe
    #ma1 : int
        #The length of the first moving average (days)
    #ma2 : int
        #The length of the second moving average (days)
    #ticker : str
        #The ticker we are plotting (for the title).
    
    
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.3,
        subplot_titles = (f'{ticker} Price', 'Volume Chart'),
        row_width = [0.3, 0.7],
    )
    
    fig.add_trace(
        go.Candlestick(
            x = df['Date'],
            open = df['Open'], 
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['Date'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['Date'], y = df[f'{ma2}_ma'], name = f'{ma2} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Bar(x = df['Date'], y = df['Volume'], name = 'Volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    

    
    return fig



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
    # XRP = rPd9oB2Kdot9HSsXSeFYpKZUV3vDsBzv73
    # DOGE = nq3ztBbL2gYz5uDeHWKe6AWXsRt19uiVHo

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
        
        #st.write(record_df.keys())
        
        assets_total = record_df[record_df.keys()[-1]].sum()
        
        
                
        #st.write(assets_total)
        col2.subheader(f"You have {amount} {coin} in this account. Its total current value is ${round(total_value_asset,2)}")

        col2.header('Wallet Collection')
        col2.dataframe(record_df)
        col2.subheader(f'The total value in your Wallet Collection is ${round(assets_total,2)}')

# Sidebar crptocurrency selector

sorted_coin = sorted(df['coin_symbol'])
selected_coin = expander_bar.multiselect('Crypotocurrency', sorted_coin, sorted_coin)

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

expander_bar.subheader('Price Data of Selected Cryptocurrency')
expander_bar.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

expander_bar.dataframe(df_coins)

# Download data to CSV
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)


#Bar plot for percentage change in price
expander_bar.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
expander_bar.dataframe(df_change)

# If statements for Bar plot time frame
col4.subheader('Barplot of % Price Change')

if percent_timeframe =='7d':
    if sort_values =='Yes':
        df_change =df_change.sort_values(by=['percent_change_7d'])
    col4.write('*7 days period*')
    plt.figure(figsize=(2,20))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col4.pyplot(plt)
elif percent_timeframe =='24h':
    if sort_values =='Yes':
        df_change =df_change.sort_values(by=['percent_change_24h'])
    col4.write('*24 hour period*')
    plt.figure(figsize=(20,50))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col4.pyplot(plt)
else:
    if sort_values =='Yes':
        df_change =df_change.sort_values(by=['percent_change_1h'])
    col4.write('*1 hour period')
    plt.figure(figsize=(20,50))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col4.pyplot(plt)


#Annual income vs Investments Pie chart
Annual_Income = st.sidebar.text_input("Please enter your Annual Income")
colors = ['green','gold']
assets_total = record_df[record_df.keys()[-1]].sum()
fig = go.Figure(data=[go.Pie(labels=['My Annual Income', 'Total Investments'],
                            values=[Annual_Income, assets_total])])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                marker=dict(colors=colors, line=dict(color='#000000', width=2)))
col2.write(fig)

        # MARC TESTING CODE
        #st.dataframe(assets_total)
#st.write('The total value in your Wallet Collection is:')
        
total_amount_ml = record_df[record_df.keys()[-1]].sum()

total_amount_ml = round(total_amount_ml,2)

#st.write(total_amount_ml)
                
# percentage of total per coin


# btc_value = record_df.query('Coins'=="ETH")

#btc_value = record_df[record_df.keys()[1].values == 'ETH']

# st.write(btc_value)

# record_df[record_df.keys()[1] == 'BTC']

#st.write('The total value of Bitcoin in your Wallet Collection is:')
#st.write(btc_value)
        
        
        
COMMON_ARGS = {
    "color": record_df.keys()[1],
    "color_discrete_sequence": px.colors.sequential.Greens,
    "hover_data": [
        record_df.keys()[0],
        record_df.keys()[1],
        record_df.keys()[2],
        record_df.keys()[3],
        record_df.keys()[4],
    ],
}  

### Pie Chart coin percentages
chart = functools.partial(st.plotly_chart, use_container_width=True)

col3.subheader("Value of each Symbol")
col3.write("Pie Chart")


pie_chart = px.pie(
    record_df, 
    values=record_df.keys()[-1], 
    names=record_df.keys()[1],
    #**COMMON_ARGS
    )

pie_chart.update_layout(margin=dict(t=0, b=0, l=0, r=0))

col3.write(pie_chart)
        
        
        
# Bar Chart of each symbol $ Value

col2.subheader("Value of each Symbol")
col2.write("Bar Chart")

bar_chart = px.bar(
    record_df, 
    y=record_df.keys()[-1], 
    x=record_df.keys()[1], 
    text=record_df.keys()[-1],
    width=1100,
    height=500
    )

bar_chart.update_traces(texttemplate='%{text:.2s}', textposition='outside')
bar_chart.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
col2.write(bar_chart)
        
# Candle stick Chart function
ticker = st.sidebar.selectbox(
    'Ticker to Plot', 
    options = ['BTC', 'ETH', 'XRP', 'DOGE']
)

days_to_plot = st.sidebar.slider(
    'Days to Plot', 
    min_value = 1,
    max_value = 300,
    value = 120,
)
ma1 = st.sidebar.number_input(
    'Moving Average #1 Length',
    value = 10,
    min_value = 1,
    max_value = 120,
    step = 1,    
)
ma2 = st.sidebar.number_input(
    'Moving Average #2 Length',
    value = 20,
    min_value = 1,
    max_value = 120,
    step = 1,    
)


# Get the dataframe and add the moving averages
df = pd.read_csv(f'{ticker}.csv')
df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
df = df[-days_to_plot:]

# Display the plotly chart on the dashboard
col2.plotly_chart(
    get_candlestick_plot(df, ma1, ma2, ticker),
    use_container_width = True,
)       
        
       
       
       
       
       
    # Coin percentage of total value

#st.subheader("Coin percentage of total value")
#st.write("Formula working brainstorm")

#record_df.sum(record_df.keys()[1] == 'BTC')

#st.write(record_df)
    
#print(df.loc['r4']['Duration'])
#print(df.loc['r4'][2])


#BTC_pct = record_df[record_df.keys()[1] == 'BTC']


#st.write(BTC_pct).sum()
    
    
    
record = {

'Address': [record_df.keys()[0]],
'Coins': [record_df.keys()[1]],
'Amount': [[record_df.keys()[2]]],
'Last Price': [[record_df.keys()[3]]],
'Total Value': [[record_df.keys()[4]]]
}
    
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
#st.write('\nBitcoin Wallet Value:\n', BTC_total_value)

btc_pct = BTC_total_value / total_amount_ml
#st.write('\Bitcoin % of Portfolio :\n', btc_pct)

ETH_total = ETH_df.sum()
ETH_total_value = ETH_total[ETH_total.keys()[-1]].sum()
#st.write('\nEthereum Wallet Value :\n', ETH_total_value)

eth_pct = ETH_total_value / total_amount_ml
#st.write('\nEthereum % of Portfolio :\n', eth_pct)


XRP_total = XRP_df.sum()
XRP_total_value = XRP_total[XRP_total.keys()[-1]].sum()
#st.write('\nRipple Wallet Value :\n', XRP_total_value)

xrp_pct = XRP_total_value / total_amount_ml
#st.write('\nRipple % of Portfolio :\n', xrp_pct)


DOGE_total = DOGE_df.sum()
DOGE_total_value = DOGE_total[DOGE_total.keys()[-1]].sum()
#st.write('\nDogecoin Wallet Value :\n', DOGE_total_value)

doge_pct = DOGE_total_value / total_amount_ml
#st.write('\nDogecoin % of Portfolio :\n', doge_pct)

coin_weights = (btc_pct, eth_pct, xrp_pct, doge_pct)

#st.write(coin_weights) 


        
        
# Monte Carlo Section

#mc_years_list = ['5', '10', '15', '20', '25', '30']

#st.write(mc_years_list)

years = col2.slider('How many years into the future do you want to see?', min_value=1, max_value=10, step=1)
Bitcoin = 'BTC-USD'
Ethereum = 'ETH-USD'
Ripple = 'XRP-USD'
Dogecoin = 'DOGE-USD'

# Download Stock Data

#st.write("# Download Stock Data")

BTC = yf.download(Bitcoin, period="max", interval="1d")
ETH = yf.download(Ethereum, period="max", interval="1d")
XRP = yf.download(Ripple, period="max", interval="1d")
DOG = yf.download(Dogecoin, period="max", interval="1d")

# Starting to clean dataframes and get them ready to concact
All_coins_hist_df = pd.concat([BTC, ETH, XRP, DOG],axis=1, keys=['BTC', 'ETH', 'XRP', 'DOG'])
All_coins_hist_df = All_coins_hist_df.dropna()

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
col2.image(img)

tbl_5yr = Monte_carlo_sim.summarize_cumulative_return()

col2.write(tbl_5yr)
        
        