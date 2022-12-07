
# **Project-1-Repo-AQML**

##### *Authors: Anthony Quiles and Marc Leipold*

## **Project Description**

### **Goal:**

#### Our goal was to creat a financial app that could be a one stop shop for all your crypto needs. This our first step to making that happen. 

### **About:**

#### We have created a financial application that can aggregate all of your wallet balances in one central and convenient place. In addition to that we have also provided you with some unique ways to look at and analyse your balances as well as a cool dashboard to let you have a snapshot of the crypto markets at a glance.

### **Example of Initial loadup**





## **Instructions**
- #### After opening application you should enter your annual income in the side bar.
- #### After entering income you will choose which network(Coin) you want to enter an address for and then enter your wallet address.
- #### Clicking the Enter button will initialize your Wallet Collection and will begin to populate all of your analyzation tools.
- #### You can also adjust the period for the top 100 coins chart for 7 days, 24hrs, or 1hr.
- #### The candlestick chart will start on a default coin but you can change it to any coin in your wallet. You can also adjust the amount of days you want in the chart and the customize up to 2 moving averages.
- #### The final function is the Monte Carlo Simulation where you can possibly have a glimpse up to 10 years in the future of your portfolio. Remember anything contained in this app is not financial advise! Do you own research;)
---
## **Wallet Aggregator**
#### The wallet aggregator was pretty straight forward and Marc did an excellent job with this. 
- #### He started first with establishing the lists we would need  as well as the network selection box and a text box to input the wallet address.
'''
{
    
    blockchain_list = ["bitcoin", "dogecoin", "ethereum", "xrp"]

    blockchain_selection = st.sidebar.selectbox("Please select the blockchain for your wallet:", blockchain_list)

    wallet_address = st.sidebar.text_input("Please enter your wallet address")

    record_df = pd.read_csv('database.csv')

    total_value_asset = None

    crypto_id = ""

    asset_weights = ""

    token = None
}
'''
- #### We also set some empty lists for the total value of all of the coins, coin id(for identification in wallet balance API), asset weights(percentage of each coin in respect to the total balance of assets), and token(this is used for the current price API for each coin).
- #### I added the record_df to store the wallet address information in a csv for easier analysis and inclusion into our visualizations.
- #### Marc created the If statements for the Network selection and I intergrated the current price call into that as well.
'''
{
        
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
}
'''
- #### Marc then created the aggregator API function using an API from [https://rest.cryptoapis.io] that initiates on the press of the 'Enter' button. I added the variables thatrepresented the cleaned data inside of this function. Since the data is in json format I dumped the json and made df's and variables from the data and sent the wallet addresses to the database.csv file. We also drop duplicates here as well to avoid doublingon the amount of specific coins. The solution to integrating the current price was a struggle to find but once Smerling suggested what we should actually do it became so simple and elegant.

'''
{

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
}
'''

- #### So this is the base of our app that we use to power almost all of the visuals that we have in our app.

---

## **Visualizations**
#### The visualizations were pretty tricky but very fun to do, they consist of a vertical bar chart, 2 pie charts, a candlestick chart, monte carlo simulation plot, and a regular bar chart.

- #### Marc was in charge of the Monte carlo plot, a bar chart representing the value of each coin, and a pie chart thatshows the percentage breakdown of all coins in the aggregator.
- #### I was in charge of a table of assets, pie chart that shows total assets vs annual income, candle stick chart with a couple of indicators, and the bar chart that shows percentage change over the last 7 day, 24hrs and 1 hr for the top 100 coins.
### **Monte Carlo**
- #### We started by adusting some of the code in MCForecastTools to make it work for cryptocurrency. I switched the trading days from 252 to 365 and I also adjusted some column names for the data being read in. After that Marc brought in some historical price data for the 4 coins in our wallet and then customized the MCSimulation to accept custom variables that the user would choose on a slider and weight variables that were calculated before hand when we cleaned the data. We printed out the resulting plot and some additional analytical information from summarize_cumulative_return() attribute.
'''
{

        # Monte Carlo Section

    #mc_years_list = ['5', '10', '15', '20', '25', '30']

    #st.write(mc_years_list)

    years = st.slider('How many years into the future do you want to see?', min_value=1, max_value=10, step=1)
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
    st.image(img)

    tbl_5yr = Monte_carlo_sim.summarize_cumulative_return()

    st.write(tbl_5yr)
}
'''
### **Pie Charts**
- #### We were both in charge of a pie chart each and they were both pretty straight forward with just different approaches and libraries of plotly.
- #### I used graph_objects in plotly to make my chart and I also included a field in the sidebar for the user to enter their annual income: 
'''
{

    #Annual income vs Investments Pie chart
    Annual_Income = st.sidebar.text_input("Please enter your Annual Income")
    colors = ['green','gold']
    assets_total = record_df[record_df.keys()[-1]].sum()
    fig = go.Figure(data=[go.Pie(labels=['My Annual Income', 'Total Investments'],
                                values=[Annual_Income, assets_total])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    col2.write(fig)
}
'''

- #### Marc used plotly express to make his pie chart to show the percentage makeup of all the coins in the portfolio:

'''
{

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
}
'''

### **Bar Charts**
- #### We were both in charge of a bar chart with Marc making one for the dollar value of each coin in the portfolio and my chart being the result of a web scraper function to display the top 100 performing coins as part of our dashboard. 
- #### Marc used plotly express for his chart with a pretty straight forward approach:
'''
{

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
}
'''

- #### The vertical bar chart I made was a bit of a challenge and we almost decided to scrap it altogether but it fell into place just in time. I had to adapt code from a web scraper made by the Data Professor that was not functioning at all. With some proper changes I was able to parse through the json data to get exactly what I needed. I had to place this code at the beggining of the file so it populates on the screen immediately and is the first thing that shows up on the dashboard. I also split the page into 4 columns and this chart sits in column 4 and goes down the length of the app.
'''
{
    
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

}
'''
- #### The following code was implemented later in the file and contains the if statements regarding what duration they want to view.
'''
{

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
}
'''
### **Candle Stick Chart**
- #### I had the Candle stick chart which involved getting historical price data for each coin in the aggregator. This code was implemented towards the beggining of the file to have this populate quickly as well as well as the general format of the chart being here too.
'''
{

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
}
'''

- #### The rest of the code for candle stick chart is towards the end of the file because I wanted it to print up after the initial analysis of you portfolio. I also icluded a select box in the sidebar so the user can pick which coin they want to view in the chart.
'''
{


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
}
'''