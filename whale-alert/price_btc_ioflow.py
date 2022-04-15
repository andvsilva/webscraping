# This script make one analysis of the 
# InFlow and OutFlow in exchanges (From-To)
# -> unknown-unknown
# -> unknwon-exchange
# -> exchange-exchange
# -> exchange-unknown

# Author: @andvsilva 2022-01-25

# libraries
import snoop
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from icecream import ic
import requests
import os
import time
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime as dt

# set the theme to the seaborn
sns.set_theme(style="darkgrid")

# column names to the dataframe price and date
name_cols = ['price_btc','date']


# set figure, canvas and subplots
fig, ax = plt.subplots(figsize = (10, 7))
fig.canvas.manager.set_window_title("On-Chain Analysis")
fig.subplots_adjust(top = 0.93, right = 0.9, bottom = 0.1, left = 0.1)

# update plot in a loop
#@snoop
def update(i):
    # get the date - time: YYYY-MM-DD HH:M:S
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    
    # get BTC price in USD
    data_BTC = requests.get('https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC').json()
    price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)
    
    # define the dataframe
    df_btc = pd.DataFrame(columns=name_cols)

    database = {'price_btc': price_btc, 
                'date': now
               }

    #print(f">>> {now} - price: {price_btc}")
    
    df_database = pd.DataFrame([database])
    df_btc = pd.concat([df_btc, df_database], ignore_index=True)
    
    # check if the file exist, please.
    if os.path.isfile('dataset/price_date.csv'):
        df_btc = df_btc.reset_index(drop=True)
        df_btc.to_csv('dataset/price_date.csv', mode='a', index=True, header=False)
    else:
        ic(df_btc)
        #df_btc = df_btc.reset_index(drop=True)
        df_btc.to_csv('dataset/price_date.csv')
    
    
    # dataframe price and date - history
    btc = pd.read_csv('dataset/price_date.csv')
    
    # convert object to pandas datetime feature.
    btc['date'] = pd.to_datetime(btc['date'])
    
    #plt.text(6, major_height+80, '@andvsilva_', dict(size=15))
    #plt.text(1.6, major_height+7, f'{now}    1 BTC - ${price_btc} USD', dict(size=16), color = 'red')
    ax.cla()
    plt.xticks(rotation=0)
    plt.grid(True)
    
    sns.lineplot(data=btc, x="date", y="price_btc", color='orange')
    
    #ax1.grid(False) # turn off grid #2
    
    ax.set_ylabel('price btc')
    ax.set_ylim(0.98*price_btc, 1.02*price_btc)
    ax.yaxis.label.set_color('black')
    ax.yaxis.label.set_fontsize(14)
    ax.tick_params(axis='y', colors='black', labelsize=14)
    ax.legend(['BTC price'], loc="upper left")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d  %H:%M:%S'))
    
    plt.savefig("../images/price_from_to.pdf", dpi=150)
    plt.savefig("../images/price_from_to.png", dpi=150)
    plt.grid(True)
    #time.sleep(10)

ani = animation.FuncAnimation(fig, update, frames = 10)

    
plt.show()