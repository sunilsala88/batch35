
import datetime as dt
#convert epoch to datetime
a=1769866207
dt1=dt.datetime.fromtimestamp(a)
print(dt1)

#datetime to epoch
c=dt.datetime.now()
epoch1=c.timestamp()
print(epoch1)

#string to datetime
a='2023-01-01'
f='%Y-%m-%d'
dt2=dt.datetime.strptime(a,f)
print(dt2)
print(dt2.year)

#datetime to string
f1='%B-%Y-%a'
s1=dt.datetime.strftime(dt1,f1)
print(s1)

s2='Jan-2026-Sat'

