
import yfinance as yf
from backtesting import Backtest, Strategy
data=yf.download('AAPL', period='5y', interval='1d',multi_level_index=False)
print(data)
import time

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
        s1=self.sma1[-1]
        s2=self.sma2[-1]
        ps1=self.sma1[-2]
        ps2=self.sma2[-2]

        if s1>s2 and ps1<=ps2:
            if self.position.is_short :
                self.position.close()
                self.buy()
            elif not self.position:
                self.buy()

        elif s1<s2 and ps1>=ps2:
            if self.position.is_long:
                self.position.close()
                self.sell()


bt=Backtest(data,firstsma,cash=1000,trade_on_close=True,commission=0.001)
output=bt.run()
print(output)   
bt.plot()