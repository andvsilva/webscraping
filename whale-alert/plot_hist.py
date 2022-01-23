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
    ax.set_ylabel('Counting', fontsize = 16)
    ax.set_ylim([0, 100])
    scale_factor = 1
    
    total_cases = database_txo.shape[0]
    
    for p in ax.patches:
       ax.annotate('{:.2f} % ({:.2f})'.format((p.get_height()/total_cases)*100, p.get_height()), (p.get_x()-0.1, p.get_height()+0.2))

    plt.xticks(rotation=10)
    plt.savefig("../images/countplot_from_to.pdf", dpi=150)
       

ani = animation.FuncAnimation(fig, update, frames = 10)

plt.show()