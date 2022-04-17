###########################################################################
# This script is using Whale Alert API
# to get real-time information about the
# transactions from blockchain

# https://whale-alert.io/ (see this for more info)

# https://pypi.org/project/whale-alert/
# https://github.com/stuianna/whaleAlert
###########################################################################

# importing libraries
import time
from datetime import datetime
from icecream import ic
import pandas as pd
from datetime import datetime
from pprint import pprint  # For formatted dictionary printing
from whalealert.whalealert import WhaleAlert
import os.path
import sys
import gc
from sys import getsizeof
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from colored import fore, back, style
import toolkit as tool
import snoop
import requests
import notify2

whale = WhaleAlert()
WhaleFund = False

# To print colored text in python 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# get key credencial for API
api_key = open("key_credencial.txt", "r").read()

# limit of transactions per request
transaction_count_limit = 1

id=0
index=0
idx=0

#from to - inflow and outflow of transactions
list_cols = ['unknown-unknown',
             'unknown-exchange',
             'exchange-unknown',
             'exchange-exchange'
            ]

dict_count_from_tos = dict()
dict_amount_usd_from_tos = dict()

for col in list_cols:
    dict_count_from_tos[col] = 0
    dict_amount_usd_from_tos[col] = 0 

df_count_from_tos = pd.DataFrame(columns=list_cols)
df_count_from_tos['']=['counting','amount_usd']
df_count_from_tos = df_count_from_tos.set_index("")

for irow in ['counting','amount_usd']:
    for jcol in list_cols:
        df_count_from_tos.loc[irow,jcol] = 0

txo_columns = ['blockchain',
               'amount_coin',
               'amount_usd',
               'hash',
               'from_to',
               'id',
               'date']

txo_columns_btc = ['blockchain',
                   'amount_coin',
                   'amount_usd',
                   'hash',
                   'from_to',
                   'id',
                   'date',
                   'price',
                   'change24h_pct']

# column names to the dataframe price and date
name_cols = ['price_btc','date']
   
while True:
    
    # dataset with the transactions.
    database_txo = pd.DataFrame(columns=txo_columns)
    
    # dataset with the transactions.
    database_txo_btc = pd.DataFrame(columns=txo_columns_btc)
    
    # check if the file exist, please.
    if os.path.isfile('dataset/database_txo.csv') and os.path.isfile('dataset/database_txo_btc.csv'):
        FileExist=True
    else:
        FileExist=False
        
    # get BTC price in USD
    data_BTC = requests.get('https://production.api.coindesk.com/v1/currency/ticker?currencies=BTC').json()
    price_btc = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['price'], 2)
    
    change24h_pct = round(data_BTC['data']['currency']['BTC']['quotes']['USD']['change24Hr']['percent'], 2)
    
    # get the date - time: YYYY-MM-DD HH:M:S
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    
    # define the dataframe
    df_btc = pd.DataFrame(columns=name_cols)

    database = {'price_btc': price_btc,
                'change24h_pct': change24h_pct,
                'date': now
               }
    
    df_database = pd.DataFrame([database])
    df_btc = pd.concat([df_btc, df_database]) #ignore_index=True
    
    # check if the file exist, please.
    if os.path.isfile('dataset/price_date.csv'):
        df_btc = df_btc.reset_index(drop=True)
        df_btc.to_csv('dataset/price_date.csv', mode='a', index=False, header=False)
    else:
        df_btc = df_btc.reset_index(drop=True)
        df_btc.to_csv('dataset/price_date.csv', index=False)
    
    # Specify a single transaction from the last 10 minutes
    start_time = int(time.time() - 600)

    readable = time.ctime()

    date_time = datetime.fromtimestamp(start_time)

    success, transactions, status = whale.get_transactions(start_time, api_key=api_key, limit=transaction_count_limit)

    if (success == 'False'):
        print("exit now, something is wrong with the request from the Whale API")
        sys.exit()

    # convert list of dict to dict
    dict_transactions = dict((key,d[key]) for d in transactions for key in d)

    # date and time of the transaction
    date_txo = datetime.fromtimestamp(dict_transactions['timestamp'])
    
    # loop in information from one transaction
    for key in dict_transactions:

        if(key == 'blockchain'):
            from_wallet = dict_transactions['from'] # dictionary
            to_wallet = dict_transactions['to'] # dictionary

            # from wallet/ owner    
            from_owner_type = from_wallet['owner_type']
            from_owner = from_wallet['owner']

            # to wallet/ owner
            to_owner_type = to_wallet['owner_type']
            to_owner = to_wallet['owner']

            # symbol and amount currency
            symbol_currency = dict_transactions['symbol']
            amount_currency = dict_transactions['amount']
            
            # hash of the transaction
            hash_txo = dict_transactions['hash']

            # amount USD
            amount_currency_usd = dict_transactions['amount_usd']

            database_txo.loc[index,'blockchain'] = symbol_currency
            database_txo.loc[index,'amount_coin'] = amount_currency
            database_txo.loc[index,'amount_usd'] = amount_currency_usd
            database_txo.loc[index,'hash'] = hash_txo

            # this is to get diferent transactions
            if(id == dict_transactions['id']):
                continue
            
            # tracking the transaction by the ID
            id = dict_transactions['id']
            
            if(symbol_currency == 'BTC'):
                database_txo_btc.loc[idx,'blockchain'] = symbol_currency
                database_txo_btc.loc[idx,'amount_coin'] = amount_currency
                database_txo_btc.loc[idx,'amount_usd'] = amount_currency_usd
                database_txo_btc.loc[idx,'hash'] = hash_txo
                
            price = round(amount_currency_usd/amount_currency, 2) # USD price cryptocurrency

            # from_to: 
            # unknown-unknown (1), 
            # unknown-exchange (2), 
            # exchange-unknown (3), 
            # exchange-exchange (4).
            from_tos = ['unknown','exchange']

            for ifrom_to in from_tos:
                for jfrom_to in from_tos:
                    if(from_owner_type == ifrom_to and to_owner_type == jfrom_to):
                        WFund = tool.whaleInfo(price, amount_currency, symbol_currency, id, date_time, WhaleFund)
                        
                        if(WFund):
                            print(fore.WHITE + back.RED + style.BOLD + f'#{index} {dict_transactions[key]}: {amount_currency} {symbol_currency} ({amount_currency_usd} USD){bcolors.ENDC}: from {bcolors.HEADER}{from_owner_type}({from_owner}) to {bcolors.HEADER}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_txo}' + style.RESET)
                            WhaleFund = False
                        else:
                            print(f'#{index} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ({amount_currency_usd} USD): from {bcolors.HEADER}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.HEADER}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_txo}')
                        
                        if(symbol_currency == 'BTC'):
                            database_txo_btc.loc[idx,'from_to'] = f'{ifrom_to}' + '-' + f'{jfrom_to}'
                            database_txo_btc.loc[idx,'id'] = id
                            database_txo_btc.loc[idx,'date'] = date_txo
                            database_txo_btc.loc[idx,'price'] = price_btc
                            database_txo_btc.loc[idx,'change24h_pct'] = change24h_pct

                            
                        dict_count_from_tos[f'{ifrom_to}-{jfrom_to}'] += 1
                        dict_amount_usd_from_tos[f'{ifrom_to}-{jfrom_to}'] = dict_amount_usd_from_tos[f'{ifrom_to}-{jfrom_to}'] + amount_currency_usd

                        print(f"Number of transactions ({ifrom_to} to {jfrom_to}).............: {dict_count_from_tos[f'{ifrom_to}-{jfrom_to}']}")
                        
                        df_count_from_tos.loc['counting',f'{ifrom_to}-{jfrom_to}'] = dict_count_from_tos[f'{ifrom_to}-{jfrom_to}']
                        df_count_from_tos.loc['amount_usd',f'{ifrom_to}-{jfrom_to}'] = dict_amount_usd_from_tos[f'{ifrom_to}-{jfrom_to}']


                        database_txo.loc[index,'from_to'] = f'{ifrom_to}' + '-' + f'{jfrom_to}'
                        database_txo.loc[index,'id'] = id
                        database_txo.loc[index,'date'] = date_txo

                        index += 1
                        idx += 1
                        
            
            if(FileExist == False):
                database_txo = database_txo.reset_index(drop=True)
                database_txo.to_csv('dataset/database_txo.csv',index=False)
                
                # BTC only
                database_txo_btc = database_txo_btc.reset_index(drop=True)
                database_txo_btc.to_csv('dataset/database_txo_btc.csv', index=False)
                
            else:
                # saving the dataframe
                database_txo = database_txo.reset_index(drop=True)
                database_txo.to_csv('dataset/database_txo.csv', mode='a', index=False, header=False)
                
                # saving the dataframe BTC only
                database_txo_btc = database_txo_btc.reset_index(drop=True)
                database_txo_btc.to_csv('dataset/database_txo_btc.csv', mode='a', index=False, header=False)
    
    tool.release_memory(database_txo)
    tool.release_memory(database_txo_btc)
    time.sleep(6)
