
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
        # print(self.data.index[-1].time())
        # print(pd.Timestamp('10:00').time())

        if self.data.index[-1].time() == pd.Timestamp('10:00').time():
            # print('inside')
            df=self.data.df
            # print(df)
            d=self.data.index[-1]
            d=pd.to_datetime(d.date())
            df=df[df.index>=d]
            self.orb_high = df.High.max()
            self.orb_low = df.Low.min()
            self.trade=0
            # print(self.orb_high, self.orb_low)

    
        if not self.position and self.orb_high and self.orb_low:
            # print('inside condition')
            if (self.data.Close[-1] > self.orb_high) and self.trade==0:
                # print('buy condition satisfied')
                p=self.data.Close[-1]
                self.buy(sl=self.orb_low)
                self.trade=1
            elif (self.data.Close[-1] < self.orb_low) and self.trade==0:
                # print('sell condition satisfied')
                self.sell(sl=self.orb_high)
                self.trade=1

        elif self.position:
            # Close position by the end of the day
            # print('i have some position')
            if self.data.index[-1].time() == pd.Timestamp('15:20').time():
                self.position.close()
                self.orb_high = None
                self.orb_low = None
                self.trade=0

        #     # print(self.position)

#alpaca data
# import pandas as pd
# df=pd.read_csv(r'/Users/algo trading 2026/batch35/20_backtesting_strategy/AMZN.csv')
# df.rename(columns={'timestamp':'Datetime','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'},inplace=True)
# df=df[['Datetime','Open','High','Low','Close','Volume']]
# #change timezone to america/new_york

# df['Datetime']=pd.to_datetime(df['Datetime'])
# df['Datetime']=df['Datetime'].dt.tz_convert('America/New_York').dt.tz_localize(None)
# df.set_index('Datetime',inplace=True)
# # keep only regular trading hours (09:30–16:00 America/New_York)
# df = df.between_time('09:30', '16:00')
# data=df.sort_index()

# data=data.iloc[-10000:]
# print(data)


import pandas as pd
df1=pd.read_csv(r'/Users/algo trading 2026/batch35/20_backtesting_strategy/TSLA.csv')
df1.rename(columns={'date':'Datetime','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'},inplace=True)
df1=df1[['Datetime','Open','High','Low','Close','Volume']]
#change timezone to america/new_york

df1['Datetime']=df1['Datetime'].str[:-6]
print(df1)
df1['Datetime']=pd.to_datetime(df1['Datetime'])
# df1['Datetime']=df1['Datetime'].dt.tz_convert('America/New_York')
df1.set_index('Datetime',inplace=True)
data=df1.sort_index()
# data=data.iloc[-3000:]
print(data)

data1=yf.download('TSLA',period='7d',interval='1m',multi_level_index=False,ignore_tz=True)
print(data1)

# # print(data)
bt = Backtest(data, ORBStrategy, cash=5000)
stats = bt.run()
print(stats)
bt.plot()