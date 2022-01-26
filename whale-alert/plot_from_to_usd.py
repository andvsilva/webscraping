# This script make one analysis of the 
# InFlow and OutFlow in exchanges (From-To)
# In USD
# Author: @andvsilva 2022-01-25
# -> unknown-unknown
# -> unknwon-exchange
# -> exchange-exchange
# -> exchange-unknown

# libraries
from turtle import width
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from icecream import ic
import requests
from datetime import datetime
import time

from_tos = ['unknown-unknown',
            'unknown-exchange',
            'exchange-unknown',
            'exchange-exchange'
           ]

sns.set_theme(style="darkgrid")

fig, ax = plt.subplots(figsize=(10,8))
fig.canvas.manager.set_window_title("On-Chain Analysis")
fig.subplots_adjust(top = 0.93, right = 0.95, bottom = 0.15, left = 0.1)

#def animate(i): ### FIXME plot animation.
now = datetime.now()

# get BTC price in USD
data_BTC = requests.get('https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC').json()
price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)

database_txo = pd.read_csv('dataset/database_txo.csv')
database_txo = database_txo.drop(columns=['Unnamed: 0'])
database_txo_usd = pd.DataFrame(columns=from_tos)

sum_amount_usd = {}

for from_to in from_tos:
    sum_amount_usd[from_to] = 0
    
for index, row in database_txo.iterrows():
    for from_to in from_tos:
        if(row['from_to'] == from_to):
            sum_amount_usd[from_to] = sum_amount_usd[from_to] + row['amount_usd']
    
for from_to in from_tos:
    sum_amount_usd[from_to] = round(sum_amount_usd[from_to],2)


#ic(sum_amount_usd)
database_txo_usd = pd.DataFrame.from_dict(sum_amount_usd, orient='index')
database_txo_usd.index.name = 'from_to'
database_txo_usd.columns = ['amount_usd']
database_txo_usd['from_to_usd'] = database_txo_usd.index
database_txo_usd.reset_index(drop=True, inplace=True)

sns.barplot(x='from_to_usd', y='amount_usd', data=database_txo_usd)
widthbars = [0.2, 0.2, 0.2, 0.2]

heights = {}
iheight = 0

for bar, newwidth in zip(ax.patches, widthbars):
    x = bar.get_x()
    width = bar.get_width()
    centre = x + width/2.
    bar.set_x(centre - newwidth/2.)
    bar.set_width(newwidth)
    heights[iheight] = bar.get_height()
    iheight += 1
    
ax.set_title('Inflow versus OutFlow in USD', fontsize = 20)
#ax.legend(loc = 'upper right', prop = {'size': 11}, ncol=2)
#ax.set_xticklabels(ax.get_xticks(), size = 0)
ax.set_xlabel('From to', fontsize = 16)
ax.set_ylabel('Amount in USD', fontsize = 16)

major_height = heights[0]

for iheight in heights:
    if(heights[iheight] >= major_height):
        major_height = heights[iheight]

plt.grid(True)
plt.xticks(rotation=10)
#plt.text(1, major_height+500, '@andvsilva_', dict(size=15))
plt.text(0.4, major_height, f'{now} 1 BTC - ${price_btc} USD', dict(size=16), color = 'red')
plt.savefig("../images/amount_from_to_usd.pdf", dpi=150)
plt.savefig("../images/amount_from_to_usd.png", dpi=150)
   
#ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()

#ax.cla()
#sns.countplot(x ='from_to', hue = "from_to", data = database_txo)
#ax.set_title(f'Inflow versus OutFlow', fontsize = 20)
#ax.legend(loc = 'upper left', prop = {'size': 12})
#ax.set_xlabel('From to', fontsize = 16)
#ax.set_ylabel('Counting', fontsize = 16)

#total_cases = database_txo.shape[0]

#heights = {}

#iheight = 0

#for p in ax.patches:
        
#    ax.annotate('{:.2f} ({:.2f} %)'.format(p.get_height(), (p.get_height()/total_cases)*100), (p.get_x()-0.1, p.get_height()+0.2))
#    heights[iheight] = p.get_height()
#    iheight += 1
    
#major_height = heights[0]

#scale_size = 1.8

#for iheight in heights:
#    if(heights[iheight] >= major_height):
#        major_height = heights[iheight]
        
#ax.set_ylim([0, major_height*scale_size])

#plt.xticks(rotation=10)
#plt.savefig("../images/countplot_from_to.pdf", dpi=150)
       

#ani = animation.FuncAnimation(fig, update, frames = 10)

#plt.show()