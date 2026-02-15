
#yfinance
import yfinance as yf
import datetime as dt

e=dt.datetime.now()
s=e-dt.timedelta(days=3)
print(s,e)
data=yf.download('TSLA',start=s,end=e,multi_level_index=False,interval='1m',ignore_tz=True)

print(data)
import mplfinance as mpf
mpf.plot(data,type='candle')