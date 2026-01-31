
import datetime 

dt1=datetime.datetime(2026,1,1)
print(dt1)

d1=datetime.timedelta(minutes=55)
dt2=dt1+d1
print(dt2)

date1=datetime.date(2021,1,1)
print(date1)
time1=datetime.time(11,15,55)
print(time1)

all_days=[]
first=datetime.datetime(2024,1,1)

for i in range(366):
    all_days.append(first)
    first=first+datetime.timedelta(days=1)

# print(all_days)

import datetime as dt
dt1=dt.datetime(2026,1,1)
print(dt1)

from datetime import datetime,timedelta
t1=datetime(2026,1,31)
print(t1)
print(t1.day)
print(t1.year)
print(t1.weekday())
#0->mon
#1->tue
#2->wed