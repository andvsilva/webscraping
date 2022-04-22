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

coindesk_api = 'https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC'

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
    database_txo = pd.read_csv('../dataset/database_txo.csv')
    database_txo = database_txo.dropna()
    
    # get BTC price in USD
    data_BTC = requests.get(coindesk_api).json()
    price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)
    
    change24h_pct = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['change24Hr']['percent'],2)
    
    # BTC only
    database_txo_btc = database_txo.loc[(database_txo['blockchain'] == 'BTC')]
    
    stats_from_to = database_txo_btc['from_to'].value_counts(normalize=True).map('{:.2%}'.format)
    stats_from_to = dict(stats_from_to)
    
    from_to_stat = {}
    
    for ifrom_to in stats_from_to:
        from_to_stat[f'{ifrom_to}'] = float(stats_from_to[ifrom_to][:-1])
    
    
    # dataframe price and date - history
    btc = pd.read_csv('../dataset/price_date.csv')
    
    # convert object to pandas datetime feature.
    btc['date'] = pd.to_datetime(btc['date'])
    
    ymax_lim = btc['price_btc'].max()
    ymin_lim = btc['price_btc'].min()
    
    coin_max = database_txo_btc['amount_coin']
    usd_max = database_txo_btc['amount_usd']
    
    idxmax = coin_max.idxmax()
    
    coin_max = coin_max.max()
    usd_max = usd_max.max()
    
    date_max = database_txo_btc.loc[idxmax, 'date']
    from_to = database_txo_btc.loc[idxmax, 'from_to']
    print(f'txo ({from_to})-> amount:  {coin_max} BTC ($ {usd_max}) USD date: {date_max}')
    
    ax.cla()
    plt.xticks(rotation=0)
    plt.grid(True)
    
    sns.lineplot(data=btc, x="date", y="price_btc", color='orange')
    
    year  = int(date_max[0:4])
    month = int(date_max[5:7])
    day   = int(date_max[8:10])
    
    # time
    HH = int(date_max[11:13])
    MM = int(date_max[14:16])
    SS = int(date_max[17:19])
        
    ax.set_title(f'{now}    1 BTC - ${price_btc} USD - change 24h: {change24h_pct}%', fontsize = 16, color='red')
    ax.set_ylabel('price (USD)')
    ax.set_ylim(0.999*ymin_lim, 1.006*ymax_lim)
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
    yscale = 1.05
    diff_space=0
    
    for ifrom_to in from_to_stat:
        plt.text(x_mean*xscale, 1.0004*ymax_lim-diff_space, f'{ifrom_to}: {from_to_stat[ifrom_to]} %', fontsize = 14)
        diff_space -= 60
    
    
    #plt.text(x_mean-0.016, 0.99*price_btc+diff_space, f'{now}    1 BTC - ${price_btc} USD - change 24h: {change24h_pct}%', dict(size=14), color = 'black')
    plt.axvline(pd.Timestamp(f'{year}-{month}-{day} {HH}:{MM}:{SS}'), ymin=0.1, ymax=0.85, color = 'red', linestyle='--', linewidth=1)
    plt.text(pd.Timestamp(f'{year}-{month}-{day} {HH}:{MM}:{SS}'), ymin_lim, f'({from_to}):  {coin_max} BTC - {date_max}', fontsize = 12, color='red')
    #plt.vlines(x=x_mean, ymin = ymin_lim, ymax= ymax_lim, colors='teal', ls='--', lw=2, label='vline_multiple - partial height')
    plt.savefig("../images/price_btc_ioflow.pdf", dpi=150)
    plt.savefig("../images/price_btc_ioflow.png", dpi=150)
    plt.grid(True)
    #time.sleep(10)

ani = animation.FuncAnimation(fig, update, frames = 10)

    
plt.show()