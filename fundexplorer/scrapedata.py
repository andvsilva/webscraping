import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.fundsexplorer.com.br/ranking"

html_text = requests.get(URL).text
print(html_text)
soup = BeautifulSoup(html_text, 'html.parser')

# get the column names
col_names = list(soup.text[23107:23482].split('\n'))

data = soup.text[23487:74907]
data_parse = list(data.split('\n'))

line_list = []
index = 0


df = pd.DataFrame(columns=col_names)

for iline in data_parse:
    if iline != '':
        line_list.append(iline)
    
    else:
        if line_list != [] and len(line_list) == 26:
            #print(line_list, len(line_list))
            #print("*" * 80)
            
            ilist = 0
            for col in col_names:
                df.loc[index, col] = line_list[ilist]
                ilist = ilist + 1
            
            ilist = 0
            line_list.clear()
    
    index = index + 1

df.to_csv('database/fiis.csv',  index=False)