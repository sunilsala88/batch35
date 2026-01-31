
import datetime as dt
#convert epoch to datetime
a=1769866207
dt1=dt.datetime.fromtimestamp(a)
print(dt1)

#datetime to epoch
c=dt.datetime.now()
epoch1=c.timestamp()
print(epoch1)