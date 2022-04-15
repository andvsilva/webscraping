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

# set the theme to the seaborn
sns.set_theme(style="darkgrid")

# column names to the dataframe price and date
name_cols = ['price_btc','date']


# set figure, canvas and subplots
fig, ax = plt.subplots(figsize = (10, 7))
fig.canvas.manager.set_window_title("On-Chain Analysis")
fig.subplots_adjust(top = 0.93, right = 0.9, bottom = 0.1, left = 0.1)

# update plot in a loop
@snoop
def update(i):
    # get the date - time: YYYY-MM-DD HH:M:S
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    
    # loading data feather format
    database_txo = pd.read_csv('dataset/database_txo.csv')
    database_txo = database_txo.drop(columns=['Unnamed: 0','amount_coin','amount_usd','id','date'])
    database_txo = database_txo.dropna()
    
    # count NaN found in the dataset
    #print(database_txo.isna().sum())
    
    # get BTC price in USD
    data_BTC = requests.get('https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC').json()
    price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)
    
    # define the dataframe
    df_btc = pd.DataFrame(columns=name_cols)

    database = {'price_btc': price_btc, 
                'date': now
               }
    
    df_database = pd.DataFrame([database])
    df_btc = pd.concat([df_btc, df_database], ignore_index=True)
    
    df_btc.to_csv('dataset/price_date.csv')
    
    # BTC only
    #database_txo_btc = database_txo.loc[(database_txo['blockchain'] == 'BTC')]
    #
    ## ETH only
    #database_txo_eth = database_txo.loc[(database_txo['blockchain'] == 'ETH')]
    
    #for idx in database_txo.index:
    #    if(isinstance(database_txo.at[idx, "from_to"], float)):
    #        continue
    #    else:
    #        database_txo.at[idx, "from_to"] += ' - ALL coins'
    #
    #for idx in database_txo_btc.index:
    #    if(isinstance(database_txo_btc.at[idx, "from_to"], float)):
    #        continue
    #    else:
    #        database_txo_btc.at[idx, "from_to"] += ' - BTC'
    #    
    #for idx in database_txo_eth.index:
    #    if(isinstance(database_txo_eth.at[idx, "from_to"], float)):
    #        continue
    #    else:
    #        database_txo_eth.at[idx, "from_to"] += ' - ETH'
    
    #database_txo_btc = database_txo_btc.drop(columns=['Unnamed: 0'])
    #database_txo_eth = database_txo_eth.drop(columns=['Unnamed: 0'])

    #database_txo = pd.concat([database_txo, database_txo_btc], ignore_index=True)
    #database_txo = pd.concat([database_txo, database_txo_eth], ignore_index=True)
    
    ax.cla()
    sns.countplot(x ='from_to', hue = "from_to", data = database_txo)
    ax.set_title('InFlow versus OutFlow - Transactions', fontsize = 15, color='blue')
    ax.set_xticklabels(ax.get_xticks(), size = 0)
    ax.set_xlabel('From to', fontsize = 16)
    ax.set_ylabel('Counting', fontsize = 16)
    ax.legend(loc = 'upper right', prop = {'size': 11}, ncol=2)
    
    total_cases = database_txo.shape[0]
    
    heights = {}
    
    iheight = 0
    
    ####################################################
    # BUG FOUNDED! FINALY
    # FIX THIS! AX.PATCHES IS ZERO! STOP THE ITERATION!
    ####################################################
    
    for p in ax.patches:    
        ax.annotate('{:.2f} ({:.2f} %)'.format(p.get_height(), (p.get_height()/total_cases)*100), (p.get_x()-0.1, p.get_height()+0.2), rotation=60)
        heights[iheight] = p.get_height()
        iheight += 1
        
    major_height = heights[0]
    ic(heights[0])
    
    scale_size = 1.8
    
    for iheight in heights:
        if(heights[iheight] >= major_height):
            major_height = heights[iheight]
            
    ax.set_ylim([0, major_height*scale_size])
    
    plt.text(6, major_height+80, '@andvsilva_', dict(size=15))
    plt.text(1.6, major_height+7, f'{now}    1 BTC - ${price_btc} USD', dict(size=16), color = 'red')
    plt.xticks(rotation=10)
    plt.grid(True)
      
    # dataframe price and date - history
    btc = pd.read_csv('dataset/price_date.csv')
    
    # set up the 2nd axis
    ax1 = ax.twinx()
    # plot bar chart on axis #2
    sns.lineplot(
        x='date', 
        y='price_btc', 
        data=btc, 
        sort=False, 
        color='black', 
        ax = ax1       # Pre-existing axes for the plot
    )
    #ax1.grid(False) # turn off grid #2
    ax1.set_ylabel('price btc')
    ax1.set_ylim(0.98*price_btc, 1.02*price_btc)
    ax1.yaxis.label.set_color('black')
    ax1.yaxis.label.set_fontsize(14)
    ax1.tick_params(axis='y', colors='black', labelsize=14)
    ax1.legend(['BTC price'], loc="upper left")
    
    plt.savefig("../images/countplot_from_to.pdf", dpi=150)
    plt.savefig("../images/countplot_from_to.png", dpi=150)
    plt.grid(True)

ani = animation.FuncAnimation(fig, update, frames = 10)

plt.show()