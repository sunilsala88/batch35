#sma,ema,macd,rsi,adx,bollinger,supertrend,atr

#talib
#pandasta
#ta

import yfinance as yf
import mplfinance as mpf
import pandas_ta as ta

data=yf.download('TSLA',period='max',multi_level_index=False)
print(data)

#sma
data['sma']=ta.sma(data['Close'])


#ema
data['ema']=ta.ema(data['Close'],length=15)


print(data)