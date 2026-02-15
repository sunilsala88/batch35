
#yfinance
import yfinance as yf
import datetime as dt

e=dt.datetime.now()
s=e-dt.timedelta(days=5)
print(s,e)
data=yf.download('TSLA',start=s,end=e,multi_level_index=False,interval='1m')
print(data)
print(data.info())
data=data.reset_index()
print(data)
data['Datetime']=data['Datetime'].dt.tz_convert("America/New_York")
data=data.set_index('Datetime')
print(data)


# # If the index is a DatetimeIndex, convert timezone directly
# data = data.tz_convert("America/New_York")
# print(data)