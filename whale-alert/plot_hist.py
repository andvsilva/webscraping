# Analysis data from Bitcointrade:
# Using web scraping to get the data.
# In this analysis:
#   - price buy/sell in the last 24 hours.
#   - book buyers/sellers
 
# Using this data from web scrape, I will
# compare the data info between buyers/sellers

# Author : Andre Vieira da Silva 2020-11-02

# libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sns.set_theme(style="darkgrid")

fig, ax = plt.subplots(figsize = (7, 6))
fig.subplots_adjust(top = 0.99, right = 0.85, bottom = 0.2, left = 0.12)
    
def update(i):
    database_txo = pd.read_csv('dataset/database_txo.csv')
    ax.cla()
    sns.countplot(x ='from_to', hue = "from_to", data = database_txo)
    ax.set_title(f'Inflow versus OutFlow', fontsize = 20)
    ax.legend(loc = 'upper left', prop = {'size': 12})
    ax.set_xlabel('From to', fontsize = 16)
    ax.set_ylabel('Frequency (%)', fontsize = 16)
    ax.set_ylim(0, 100)
    plt.xticks(rotation=10)
    
    total_cases = database_txo.shape[0]
    
    for p in ax.patches:
       ax.annotate('{:.2f} %'.format((p.get_height()/total_cases)*100), (p.get_x()+0.25, p.get_height()+0.01))
       
    plt.savefig("../images/countplot_from_to.pdf", dpi=150)
       

ani = animation.FuncAnimation(fig, update, frames = 10)
#ani.save('test.mp4', dpi=200, fps=1)

plt.show()


# count plot on single categorical variable
#plt.xticks(rotation=15)
#plt.ylim(0,15)
#plt.xlabel('From to')
#plt.ylabel('Frequency')
## Show the plot
#plt.show(block=False)
#plt.pause(20)
#plt.close()
#plt.pause(20)