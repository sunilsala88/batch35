

import datetime




import pandas as pd
import requests

url = 'https://kslindia.com/nse-holidays-for-2025/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

response = requests.get(url, headers=headers)
df7 = pd.read_html(response.text)
df7=df7[0]
holidays=df7['Date'].to_list()
# print(holidays)
dt_holidays=[]
for h in holidays:
    dt_holidays.append(datetime.datetime.strptime(h, '%B %d, %Y'))
print(dt_holidays)


all_thursday=[]
first=datetime.datetime(2025,1,1)

for i in range(366):

    first=first+datetime.timedelta(days=1)
    if first.weekday()==3:
        if first in dt_holidays:
            temp=first-datetime.timedelta(days=1)
            all_thursday.append(temp)
        else:
            all_thursday.append(first)

print(all_thursday)