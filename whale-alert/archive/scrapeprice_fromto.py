# In this script we will create
# one on chain analysis to see if there 
# exist Correlaction between the price
# and from to (exchange->exchange
#              exchange->unknown
#              unknown->unknown
#              unknown->exchange) for the BTC.

# author: @andvsilva qua 06 abr 2022 18:58:19

############## importing libraries ########################################
import time
from datetime import datetime
from icecream import ic
import pandas as pd
from datetime import datetime
from pprint import pprint  # For formatted dictionary printing
from whalealert.whalealert import WhaleAlert
import notify2
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

list_cols = ['unknown-unknown',
             'unknown-exchange',
             'exchange-unknown',
             'exchange-exchange'
            ]

while True:
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

            # this is to get diferent transactions
            if(id == dict_transactions['id'] and symbol_currency == 'BTC'):
                print('BTC transaction...')
            else:
                continue
            
            # tracking the transaction by the ID
            id = dict_transactions['id']

            # amount USD
            amount_currency_usd = dict_transactions['amount_usd']

            price = round(amount_currency_usd/amount_currency, 2) # USD price cryptocurrency

            print(f'#{index} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ($ {amount_currency_usd} USD): from {bcolors.HEADER}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.HEADER}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_time}')
            
            index += 1
            
    time.sleep(6)