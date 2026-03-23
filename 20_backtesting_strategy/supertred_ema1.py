

import yfinance as yf
data=yf.download('BTC-USD', period='2y', interval='1d',multi_level_index=False)
print(data)

from backtesting import Backtest, Strategy

import pandas_ta as ta

def get_ema(close,period):
    d=ta.ema(close,period=period)
    return (d)

def get_adx(high,low,close,l):
    d=ta.adx(high,low,close,length=l)
    return d[f'ADX_{l}']

def get_supertrend(high,low,close,l):
    d=ta.supertrend(high,low,close,l)
    return d[f'SUPERTd_{l}_3.0']

def get_supertrend_value(high,low,close,l):
    d=ta.supertrend(high,low,close,l)
    return d[f'SUPERT_{l}_3.0']

class super_ema(Strategy):
    e1=5
    s1=15
    d1=14
    th1=30


    def init(self):
        closing_price=self.data.Close.s
        high_price=self.data.High.s
        low_price=self.data.Low.s
        self.ema1=self.I(get_ema,closing_price,self.e1)
        self.supertrend=self.I(get_supertrend,high_price,low_price,closing_price,self.s1)
        self.supertrend_value=self.I(get_supertrend_value,high_price,low_price,closing_price,self.s1)
        self.adx=self.I(get_adx,high_price,low_price,closing_price,self.d1)
        self.current_trend=0
        self.trade_taken_in_trend=False
    def next(self):
        closing_price=self.data.Close[-1]

        if self.supertrend[-1]>0:
            trend=1
        elif self.supertrend[-1]<0:
            trend=-1
        else:
            trend=0

        if trend!=self.current_trend:
            self.current_trend=trend
            self.trade_taken_in_trend=False

        if self.supertrend[-1]>0 and closing_price>self.ema1[-1] and self.adx[-1]>self.th1 and not self.trade_taken_in_trend:
            
            if self.position.is_short :
                self.position.close()
                self.buy(sl=closing_price*0.95)
                self.trade_taken_in_trend=True
            elif not self.position:
                self.buy(sl=closing_price*0.95)
                self.trade_taken_in_trend=True
        elif self.supertrend[-1]<0 and closing_price<self.ema1[-1] and self.adx[-1]>self.th1 and not self.trade_taken_in_trend:
            if self.position.is_long:
                self.position.close()
                self.sell(sl=closing_price*1.05)
                self.trade_taken_in_trend=True
            elif not self.position:
                self.sell(sl=closing_price*1.05)
                self.trade_taken_in_trend=True

# e1=get_ema(data['Close'],20)
s1=get_adx(data['High'], data['Low'], data['Close'],20)
print(s1.tail(20))


bt=Backtest(data,super_ema,cash=500_000,trade_on_close=True,finalize_trades=True)
output=bt.run()
print(output)   
bt.plot()

# stats = bt.optimize(e1=range(5,50,3),
#                     s1=range(10,70,5),
#                     d1=range(10,30,3),
#                     th1=range(15,35,4),  
#                     maximize='Return [%]')
# print(stats)
# print(stats['_strategy'])

# stats['_trades'].to_csv('trades.csv')
# bt.plot()