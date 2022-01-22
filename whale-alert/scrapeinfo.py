###########################################################################
# This script is using Whale Alert API
# to get real-time information about the
# transactions from blockchain

# https://whale-alert.io/ (see this for more info)

# https://pypi.org/project/whale-alert/
# https://github.com/stuianna/whaleAlert
###########################################################################

############## importing libraries ########################################
import time
from datetime import datetime
from icecream import ic
import pandas as pd
from datetime import datetime
from pprint import pprint  # For formatted dictionary printing
from whalealert.whalealert import WhaleAlert
import notify2
import sys
whale = WhaleAlert()

# Building a desktop notification tool for Linux using python
# https://www.codementor.io/@dushyantbgs/building-a-desktop-notification-tool-using-python-bcpya9cwh
def notify(price, symbol_currency, date_time):

    ICON_PATH = "../images/btc.jpg" # This is not working, FIXME, I do not know why.

    # initialise the d-bus connection
    notify2.init("Cryptocurrency reach the price")

    # create Notification object
    n = notify2.Notification("Crypto Notifier", icon = ICON_PATH)

    # Set the urgency level
    n.set_urgency(notify2.URGENCY_NORMAL)

    # Set the timeout
    n.set_timeout(1000)

    result = str(price)

    # Update the content
    n.update(f"1 {symbol_currency} in USD date: {date_time}", result)

    # Show the notification
    n.show()

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
i=0

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

list_limits = [100]
list_symbols = ['BTC', 'ETH']

def whaleInfo(amount_currency, symbol_currency, id, date_time):
    for ilist_symbol in list_symbols:
        if symbol_currency == f'{ilist_symbol}':
            for ilist_limit in list_limits:
                if( amount_currency >= ilist_limit):
                    notify(price, symbol_currency, date_time)
                    print('***********************************************************************************')
                    print('>>>>>>>>>> WARNING: WHALE MOVING FUNDS <<<<<<<<<<<<<')
                    print(f'MORE THAN {ilist_limit} {ilist_symbol} MOVED - ID: {id}')
                    print('***********************************************************************************')

while True:
    # Specify a single transaction from the last 10 minutes
    start_time = int(time.time() - 600)

    readable = time.ctime()

    date_time = datetime.fromtimestamp(start_time)
    #print("date_time:",date_time)

    success, transactions, status = whale.get_transactions(start_time, api_key=api_key, limit=transaction_count_limit)

    if (success == 'False'):
        print("exit now, something is wrong.")
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

            # amount USD
            amount_currency_usd = dict_transactions['amount_usd']

            # this is to get diferent transactions
            if(id == dict_transactions['id']):
                continue
            
            # tracking the transaction by the ID
            id = dict_transactions['id']

            price = round(amount_currency_usd/amount_currency, 2) # USD price cryptocurrency

            # from_to: unknown-unknown (1), unknown-exchange (2), exchange-unknown (3), exchange-exchange (4)
            from_tos = ['unknown','exchange']

            for ifrom_to in from_tos:
                for jfrom_to in from_tos:
                    if(from_owner_type == ifrom_to and to_owner_type == jfrom_to):
                        whaleInfo(amount_currency, symbol_currency, id, date_time)
                        print(f'#{i} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ({amount_currency_usd} USD): from {bcolors.HEADER}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.HEADER}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_time}')
                        
                        dict_count_from_tos[f'{ifrom_to}-{jfrom_to}'] += 1
                        dict_amount_usd_from_tos[f'{ifrom_to}-{jfrom_to}'] = dict_amount_usd_from_tos[f'{ifrom_to}-{jfrom_to}'] + amount_currency_usd

                        print(f"Number of transactions ({ifrom_to} to {jfrom_to}).............: {dict_count_from_tos[f'{ifrom_to}-{jfrom_to}']}")
                        i += 1
                        df_count_from_tos.loc['counting',f'{ifrom_to}-{jfrom_to}'] = dict_count_from_tos[f'{ifrom_to}-{jfrom_to}']
                        df_count_from_tos.loc['amount_usd',f'{ifrom_to}-{jfrom_to}'] = dict_amount_usd_from_tos[f'{ifrom_to}-{jfrom_to}']
            
            ic(df_count_from_tos)
    time.sleep(6)
