
import yfinance as yf
from backtesting import Backtest, Strategy
data=yf.download('AAPL', period='5y', interval='1d',multi_level_index=False)
print(data)


def get_sma(close,period):
    return close.rolling(window=period).mean()


class firstsma(Strategy):
    s1=20
    s2=50

    def init(self):
        closing_price=self.data.Close.s
        self.sma1=self.I(get_sma,closing_price,self.s1)
        self.sma2=self.I(get_sma,closing_price,self.s2)
    def next(self):
        pass

sma1=get_sma(data['Close'],5)
print(sma1)

bt=Backtest(data,firstsma)
output=bt.run()
print(output)   
bt.plot()