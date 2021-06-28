###########################################################################
# This script is using Whale Alert API
# to get real-time information about the
# transactions from blockchain

# https://whale-alert.io/ (see this for more info)

# https://pypi.org/project/whale-alert/
# https://github.com/stuianna/whaleAlert
###########################################################################

# To print colored text in python 
#class bcolors:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKCYAN = '\033[96m'
#    OKGREEN = '\033[92m'
#    WARNING = '\033[93m'
#    FAIL = '\033[91m'
#    ENDC = '\033[0m'
#    BOLD = '\033[1m'
#    UNDERLINE = '\033[4m'

############## importing libraries ########################################
import time
from icecream import ic
import pandas as pd
from datetime import datetime
from pprint import pprint  # For formatted dictionary printing
from whalealert.whalealert import WhaleAlert
whale = WhaleAlert()

# Specify a single transaction from the last 10 minutes
start_time = int(time.time() - 600)

# get key credencial for API
api_key = open("key_credencial.txt", "r").read()

# limit of transactions per request
transaction_count_limit = 1

success, transactions, status = whale.get_transactions(start_time, api_key=api_key, limit=transaction_count_limit)

print(transactions)