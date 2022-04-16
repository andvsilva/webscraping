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

# set figure, canvas and subplots
fig, ax = plt.subplots(figsize = (10, 7))
fig.canvas.manager.set_window_title("On-Chain Analysis")
fig.subplots_adjust(top = 0.93, right = 0.9, bottom = 0.1, left = 0.1)

# update plot in a loop
#@snoop
def update(i):
    # get the date - time: YYYY-MM-DD HH:M:S
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    
    # loading data feather format
    database_txo = pd.read_csv('dataset/database_txo.csv')
    database_txo = database_txo.drop(columns=['Unnamed: 0','amount_coin','amount_usd','id','date'])
    database_txo = database_txo.dropna()
    
    # get BTC price in USD
    data_BTC = requests.get('https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC').json()
    price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)
    
    change24Hr_pct = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['change24Hr']['percent'],2)
    
    # BTC only
    database_txo_btc = database_txo.loc[(database_txo['blockchain'] == 'BTC')]
    
    stats_from_to = database_txo_btc['from_to'].value_counts(normalize=True).map('{:.2%}'.format)
    stats_from_to = dict(stats_from_to)
    
    from_to_stat = {}
    
    for ifrom_to in stats_from_to:
        from_to_stat[f'{ifrom_to}'] = float(stats_from_to[ifrom_to][:-1])
    
    
    # dataframe price and date - history
    btc = pd.read_csv('dataset/price_date.csv')
    
    # convert object to pandas datetime feature.
    btc['date'] = pd.to_datetime(btc['date'])
    
    #plt.text(6, major_height+80, '@andvsilva_', dict(size=15))
    
    ax.cla()
    plt.xticks(rotation=0)
    plt.grid(True)
    
    sns.lineplot(data=btc, x="date", y="price_btc", color='orange')
    
    #ax1.grid(False) # turn off grid #2
    
    ax.set_title('InFlow versus OutFlow - Transactions vs Price BTC', fontsize = 15, color='blue')
    ax.set_ylabel('price (USD)')
    ax.set_ylim(0.99*price_btc, 1.005*price_btc)
    ax.yaxis.label.set_color('black')
    ax.yaxis.label.set_fontsize(14)
    ax.tick_params(axis='y', colors='black', labelsize=14)
    ax.legend(['BTC'], loc="upper left")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d  %H:%M:%S'))
    
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)
    
    xmin, xmax, ymin, ymax = plt.axis()
    
    x_mean = (xmax+xmin)/2
    y_mean = (ymax+ymin)/2
    
    xscale = 1.0
    yscale = 1.0
    diff_space=70
    
    for ifrom_to in from_to_stat:
        plt.text(x_mean*xscale, y_mean*yscale+diff_space, f'{ifrom_to}: {from_to_stat[ifrom_to]} %', fontsize = 14)
        diff_space += 30
        #xscale = xscale*1.005
        #yscale = yscale*1.001
        
    plt.text(x_mean-0.024, y_mean-100, f'{now}    1 BTC - ${price_btc} USD - change 24h: {change24Hr_pct}%', dict(size=14), color = 'black')
    plt.savefig("../images/price_from_to.pdf", dpi=150)
    plt.savefig("../images/price_from_to.png", dpi=150)
    plt.grid(True)
    #time.sleep(10)

ani = animation.FuncAnimation(fig, update, frames = 10)

    
plt.show()