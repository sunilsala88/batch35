
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
    slp=0.04

    def init(self):
        closing_price=self.data.Close.s
        self.sma1=self.I(get_sma,closing_price,self.s1)
        self.sma2=self.I(get_sma,closing_price,self.s2)
    def next(self):
        closeing_price=self.data.Close[-1]
        s1=self.sma1[-1]
        s2=self.sma2[-1]
        ps1=self.sma1[-2]
        ps2=self.sma2[-2]

        if s1>s2 and ps1<=ps2:
            if self.position.is_short :
                self.position.close()
                self.buy(sl=closeing_price*(1-self.slp))
            elif not self.position:
                self.buy(sl=closeing_price*(1-self.slp))

        elif s1<s2 and ps1>=ps2:
            if self.position.is_long:
                self.position.close()
                self.sell(sl=closeing_price*(1+self.slp))


bt=Backtest(data,firstsma,cash=1000,trade_on_close=True,commission=0.001)
output=bt.run()
print(output)   
# bt.plot()

stats = bt.optimize(s1=[5,10,15,20,25,30,35,40],
                    s2=range(50,100,5),
                    slp=[0.03,0.04,0.05,0.06,0.07,0.08,0.09],
                    maximize='Win Rate [%]')
print(stats)
print(stats['_strategy'])

stats['_trades'].to_csv('trades.csv')
bt.plot()