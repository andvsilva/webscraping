# libraries
import os

# whale alert api package
from whalealert.whalealert import WhaleAlert
import time

# set object whale
whale = WhaleAlert()

# set the api key
api_key = 'jlo1G5L7K4CBNcw557uOGOzDrq1i7Oca'

# limit of transactions to make the request is 1 for free plan
transaction_count_limit = 1

# For the free plan the number of requests 
# is limited to 10 per minute. 
start_time = int(time.time() - 600)

# the request to the whale alert
success, transactions, status = whale.get_transactions(start_time,  
                                                       api_key=api_key, 
                                                       limit=transaction_count_limit
                                                      )

# result - transaction
print('\n')
print(transactions)
