
from  ib_async import *
import pendulum as dt
import time
import logging
import pandas as pd
time_zone='America/New_York'
ct= dt.now(time_zone)
print(ct)


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=18)


tickers = ['ETH','AAVE','BCH','LTC']
# tickers=["TSLA","AAPL","MSFT"]
exchange='PAXOS' #SMART
currency='USD' #USD
account_no='DUH316001'
ord_validity='GTC'
quantity=1
#start time
start_hour,start_min=10,41
#end time
end_hour,end_min=14,59
candle_time_frame=1





contract_objects={}
for ticker in tickers:
    c=ib.qualifyContracts(Crypto(ticker,exchange, currency))[0]
    print(c)
    contract_objects[ticker]=c
print(contract_objects)


class PendulumFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = dt.from_timestamp(record.created, tz=time_zone)
        if datefmt:
            return ct.strftime(datefmt)
        return ct.format('YYYY-MM-DD HH:mm:ss ZZ')


log_filename = f'strategy_{dt.now(time_zone).to_date_string()}.log'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
handler.setLevel(logging.INFO)
handler.setFormatter(PendulumFormatter("%(asctime)s - %(message)s"))
logger.addHandler(handler)

logger.info(f"Current time: {dt.now(time_zone)} - Strategy started")


def get_historical_data(ticker_contract,bar_size,duration):
    logger.info('fetching historical data')
    bars = ib.reqHistoricalData(
    ticker_contract, endDateTime='', durationStr=duration,
    barSizeSetting=bar_size, whatToShow='MIDPOINT', useRTH=True,formatDate=1)
    # convert to pandas dataframe:
    df = util.df(bars)
    df['ema']=df['close'].ewm(span=10).mean()
    df['sma']=df['close'].rolling(window=20).mean()
    logger.info('calculated indicators')
    return df


def get_info_about_position(pos,ticker_name):
     """ this function takes postion and ticker_name as input if i am long give 1,for short give -1, if no position or 0 quantity give 0"""
     #     #  c1=Stock(ticker_name, 'SMART', 'USD')
     c1=contract_objects.get(ticker_name)
     for p in pos:
         if p.contract.symbol == c1.symbol:
             if p.position > 0:
                 return 1
             elif p.position < 0:
                 return -1
             else:
                 return 0
     return 0


def check_market_order_placed(name):
    """Returns True if an open market order exists for the given ticker, False otherwise."""
    open_orders = ib.openOrders()
    for order in open_orders:
        if order.contract.symbol == name and order.orderType == 'MKT':
            return True
    return False


def trade_buy_crypto(ticker_name):
    if check_market_order_placed(ticker_name):
        logger.info(f'market order already placed for {ticker_name} so skipping placing new order')
        print(f'market order already placed for {ticker_name} so skipping placing new order')
        return 0
    logger.info(f'placing buy order for {ticker_name}')
    c1=contract_objects.get(ticker_name)
    order = MarketOrder('BUY', quantity, account=account_no)
    trade = ib.placeOrder(c1, order)
    logger.info(f'buy order placed for {ticker_name}')
    return trade

def strategy_condition(df,ticker):
    
    buy_condition=df['ema'].iloc[-1]>df['sma'].iloc[-1] and df['ema'].iloc[-2]<df['sma'].iloc[-2]
    buy_condition=True
    logger.info(f'checking strategy condition for {ticker}')
    if buy_condition:
        logger.info(f'buy condition satisfied for {ticker}')
        print(f'buy condition satisfied for {ticker}')
        # place buy order here
        trade_buy_crypto(ticker)


def main_strategy_code():
    print("inside main strategy")
    logger.info(f"inside main strategy {tickers}")
    pos=ib.positions(account=account_no)
    print(pos)

    ord=ib.openOrders()
    print(ord)

    for ticker in tickers:
        c=contract_objects[ticker]
        print(c)
        df=get_historical_data(c,'1 min','3 D')
        print(df)
        current_price=df['close'].iloc[-1]
        print(current_price)



        capital=int(float([v for v in ib.accountValues(account=account_no) if v.tag == 'AvailableFunds' ][0].value))
        print(capital)
        quantity=int((capital/10)/current_price)  
        print(quantity)
        logger.info('Checking condition')

        position_status=get_info_about_position(pos,ticker)

        if quantity==0:
            logger.info('we dont have enough money so we cannot trade')
            continue

        if position_status==0:
            print('we dont have any position')
            logger.info('we dont have any position') 
            strategy_condition(df,ticker)

            
        elif position_status!=0:
            logger.info('we have some position and current ticker is in position')
            print('we have some position and current ticker is in position')

            if position_status==1:
                logger.info('we have current ticker in position and is long')
                print('we have current ticker in position and is long')




def main():

    while True:
        ct= dt.now(time_zone)
        print(ct)
        #run every 5 min
        # if ct.second==1 and ct.minute%5==0:
        if ct.second==1:
            print('new candle started')
            main_strategy_code()
        time.sleep(1)
        
        

# main()




#function which will run every min
#fetch my postion,check your orders
#check the price of the stock
#check how money we have
#check entry and exit rules
#place order if entry rules are satisfied
#close position if exit rules are satisfied