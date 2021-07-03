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
def notify(price):

    ICON_PATH = "628px-Ethereum_logo_2014.svg.png"

    # initialise the d-bus connection
    notify2.init("Cryptocurrency reach the price")

    # create Notification object
    n = notify2.Notification("Crypto Notifier", icon = ICON_PATH)

    # Set the urgency level
    # options:
    # -> notify2.URGENCY_LOW
    # -> notify2.URGENCY_NORMAL
    # -> notify2.URGENCY_HIGH
    n.set_urgency(notify2.URGENCY_NORMAL)

    # Set the timeout
    n.set_timeout(1000)

    result = str(price)

    # Update the content
    n.update("Current price USD", result)

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
count_unknown_to_unknown = 0
count_exchange_to_unknown = 0
count_exchange_to_exchange = 0
count_unknown_to_exchange = 0

list_limits = [2000, 1000]
list_symbols = ['BTC', 'ETH']

def whaleInfo(amount_currency, symbol_currency):
    for ilist_symbol in list_symbols:
        if symbol_currency == f'{ilist_symbol}':
            for ilist_limit in list_limits:
                if( amount_currency >= ilist_limit):
                    notify(price)
                    print('***********************************************************************************')
                    print('>>>>>>>>>> WARNING: WHALE MOVING FUNDS <<<<<<<<<<<<<')
                    print(f'MORE THAN {ilist_limit} {ilist_symbol} MOVED')
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

            id = dict_transactions['id']

            price = round(amount_currency_usd/amount_currency, 2) # USD price cryptocurrency

            # wallet: unknown to unknown
            if(from_owner_type == "unknown" and to_owner_type == "unknown"):
                whaleInfo(amount_currency, symbol_currency)
                print(f'#{i} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ({amount_currency_usd} USD): from {bcolors.HEADER}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.HEADER}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_time}')
                count_unknown_to_unknown = count_unknown_to_unknown + 1
                print(f"Number of transactions (unknown to unknown).............: {count_unknown_to_unknown}")
                i = i + 1
            
            # wallet: exchange to unknown
            if(from_owner_type == "exchange" and to_owner_type == "unknown"):
                whaleInfo(amount_currency, symbol_currency)
                print(f'#{i} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ({amount_currency_usd} USD): from {bcolors.OKGREEN}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.OKGREEN}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_time}')
                count_exchange_to_unknown = count_exchange_to_unknown + 1
                print(f"Number of transactions (exchange to unknown).............: {count_exchange_to_unknown}")
                i = i + 1

            # wallet: exchange to exchange
            if(from_owner_type == "exchange" and to_owner_type == "exchange"):
                whaleInfo(amount_currency, symbol_currency)
                print(f'#{i} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ({amount_currency_usd} USD): from {bcolors.OKGREEN}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.OKGREEN}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_time}')
                count_exchange_to_exchange = count_exchange_to_exchange + 1
                print(f"Number of transactions (exchange to exchange).............: {count_exchange_to_exchange}")
                i = i + 1

            # wallet: unknown to exchange
            if(from_owner_type == "unknown" and to_owner_type == "exchange"):
                whaleInfo(amount_currency, symbol_currency)
                print(f'#{i} {bcolors.HEADER}{dict_transactions[key]}{bcolors.ENDC}: {bcolors.OKGREEN}{amount_currency} {symbol_currency}{bcolors.ENDC} ({amount_currency_usd} USD): from {bcolors.FAIL}{from_owner_type}({from_owner}){bcolors.ENDC} to {bcolors.FAIL}{to_owner_type}({to_owner}){bcolors.ENDC} id: {id}, {date_time}')
                count_unknown_to_exchange = count_unknown_to_exchange + 1
                print(f"Number of transactions (unknown to exchange).............: {count_unknown_to_exchange}")
                i = i + 1


    time.sleep(8)