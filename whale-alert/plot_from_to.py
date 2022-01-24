# This script make one analysis of the 
# InFlow and OutFlow in exchanges (From-To)
# -> unknown-unknown
# -> unknwon-exchange
# -> exchange-exchange
# -> exchange-unknown

# Author : Andre Vieira da Silva 2020-11-02

# libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from icecream import ic
import requests

data_BTC = requests.get('https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC').json()

sns.set_theme(style="darkgrid")

fig, ax = plt.subplots(figsize = (10, 7))
fig.subplots_adjust(top = 0.93, right = 0.9, bottom = 0.1, left = 0.1)
    
def update(i):
    
    now = datetime.now()
    
    database_txo = pd.read_csv('dataset/database_txo.csv')
    
    price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)
    
    database_txo= database_txo.drop(columns=['amount_coin','amount_usd','id','date'])
    
    # BTC only
    database_txo_btc = database_txo.loc[(database_txo['blockchain'] == 'BTC')]
    database_txo_eth = database_txo.loc[(database_txo['blockchain'] == 'ETH')]
    
    
    for i in database_txo_btc.index:
        database_txo_btc.at[i, "from_to"] += ' - BTC'
        
    for i in database_txo_eth.index:
        database_txo_eth.at[i, "from_to"] += ' - ETH'
    
    database_txo_btc = database_txo_btc.drop(columns=['Unnamed: 0'])
    database_txo_eth = database_txo_eth.drop(columns=['Unnamed: 0'])
    
    database_txo = database_txo.append(database_txo_btc)
    database_txo = database_txo.append(database_txo_eth)
    
    ax.cla()
    sns.countplot(x ='from_to', hue = "from_to", data = database_txo)
    ax.set_title(f'{now}  Inflow versus OutFlow - 1 BTC - {price_btc} USD', fontsize = 15, color='blue')
    ax.legend(loc = 'upper left', prop = {'size': 11}, ncol=2)
    ax.set_xticklabels(ax.get_xticks(), size = 0)
    ax.set_xlabel('From to', fontsize = 16)
    ax.set_ylabel('Counting', fontsize = 16)

    total_cases = database_txo.shape[0]
    
    heights = {}
    
    iheight = 0
    
    for p in ax.patches:
            
        ax.annotate('{:.2f} ({:.2f} %)'.format(p.get_height(), (p.get_height()/total_cases)*100), (p.get_x()-0.1, p.get_height()+0.2), rotation=35)
        heights[iheight] = p.get_height()
        iheight += 1
        
    major_height = heights[0]
    
    scale_size = 1.8
    
    for iheight in heights:
        if(heights[iheight] >= major_height):
            major_height = heights[iheight]
            
    ax.set_ylim([0, major_height*scale_size])
    
    plt.xticks(rotation=10)
    plt.savefig("../images/countplot_from_to.pdf", dpi=150)
    plt.savefig("../images/countplot_from_to.png", dpi=150)
       

ani = animation.FuncAnimation(fig, update, frames = 10)

plt.show()