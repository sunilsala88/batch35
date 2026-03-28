
from backtesting import Backtest, Strategy
import pandas as pd
import yfinance as yf
import time



class ORBStrategy(Strategy):
    
    def init(self):
        self.orb_high = None
        self.orb_low = None
        self.trade=0


    def next(self):
        print(self.data.index[-1].time())
        print(pd.Timestamp('10:00').time())

        if self.data.index[-1].time() == pd.Timestamp('01:00').time():
            print('inside')
            df = self.data.df
            # Build timezone-aware day boundaries to avoid tz-naive vs tz-aware comparisons
            cur_ts = self.data.index[-1]
            today = cur_ts.normalize()
            yesterday = today - pd.Timedelta(days=1)
            df_prev = df[(df.index >= yesterday) & (df.index < today)]
            if not df_prev.empty:
                self.orb_high = df_prev.High.max()
                self.orb_low = df_prev.Low.min()
                self.trade = 0
            # print(df_prev)
            # print(self.orb_high, self.orb_low)


    
        if not self.position and self.orb_high and self.orb_low:
            # print('inside condition')
            if (self.data.Close[-1] > self.orb_high) and self.trade==0:
                # print('buy condition satisfied')
                p=self.data.Close[-1]
                self.buy()
                self.trade=1
            elif (self.data.Close[-1] < self.orb_low) and self.trade==0:
                # print('sell condition satisfied')
                self.sell()
                self.trade=1

        elif self.position:
            # Close position by the end of the day
            # print('i have some position')
            if self.data.index[-1].time() == pd.Timestamp('23:00').time():
                self.position.close()
                self.orb_high = None
                self.orb_low = None
                self.trade=0




            # print(self.position)



import yfinance as yf
data=yf.download('BTC-USD',period='6mo',interval='1h',multi_level_index=False)
print(data.head(20))



# print(data)
bt = Backtest(data, ORBStrategy, cash=300_000,trade_on_close=True)
stats = bt.run()
print(stats)
bt.plot()

