
import datetime

from  ib_async import *
import pendulum as dt
import time
import logging
import pandas as pd
time_zone='Asia/Kolkata'
ct= dt.now(time_zone)
print(ct)


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=18)

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




tickers = ['RELIANCE','AXISBANK','HDFCBANK','KOTAKBANK']
exchange='NSE'
currency='INR'
account_no='DU6327991'
ord_validity='DAY'
quantity_=1

start_hour,start_min=19,2
end_hour,end_min=19,10


contract_objects={}
for ticker in tickers:
    c=ib.qualifyContracts(Stock(ticker,exchange, currency))[0]
    print(c)
    contract_objects[ticker]=c
print(contract_objects)



def close_ticker_postion(name):
    pos=ib.positions(account=account_no)
    if pos:
        df2=util.df(pos)
        df2['ticker_name']=[cont.symbol for cont in df2['contract']]
        cont=contract_objects[name]
        filtered=df2[df2['ticker_name']==name]
        if filtered.empty:
            logging.info(f'No open position found for {name}, skipping close')
            return
        quant=filtered.position.iloc[0]
        print(cont)
        print(quant)
        if quant>0:
            #sell
            ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=abs(quant),action='SELL',account=account_no,tif=ord_validity)
            ib.placeOrder(cont,ord)
            logging.info('Closing position SELL '+name)
          
        elif quant<0:
            #buy
            ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=abs(quant),action='BUY',account=account_no,tif=ord_validity)
            ib.placeOrder(cont,ord)
            logging.info('Closing position BUY '+name)

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
    ord=ib.openTrades()
    if ord:
        ord_df=util.df(ord)
        ord_df['name']=[c.symbol for c in ord_df['contract']]
        ord_df['ord_type']=[c.orderType for c in ord_df['order']]
        a=ord_df[(ord_df['name']==name) & (ord_df['ord_type']=='MKT')]
        if a.empty:
            return True
        else:
            return False
    else:
        return True

def trade_buy_stocks(stock_name, quantity):
    contract = contract_objects[stock_name]
    if check_market_order_placed(stock_name):
        ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=quantity,action='BUY',account=account_no,tif=ord_validity)
        trade=ib.placeOrder(contract,ord)
        elapsed=0
        while trade.orderStatus.status not in ('Filled','ApiCancelled','Cancelled') and elapsed<15:
            ib.sleep(1)
            elapsed+=1
        if trade.orderStatus.status != 'Filled':
            logger.error(f'BUY market order not filled within timeout (status={trade.orderStatus.status})')
            return
        logger.info(trade)
        logger.info('Placed market buy order')
    else:
        logger.info('market order already placed')
        print('market order already placed')
        return 0

def trade_sell_stocks(stock_name, quantity):
    contract = contract_objects[stock_name]
    if check_market_order_placed(stock_name):
        ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=quantity,action='SELL',account=account_no,tif=ord_validity)
        trade=ib.placeOrder(contract,ord)
        elapsed=0
        while trade.orderStatus.status not in ('Filled','ApiCancelled','Cancelled') and elapsed<15:
            ib.sleep(1)
            elapsed+=1
        if trade.orderStatus.status != 'Filled':
            logger.error(f'SELL market order not filled within timeout (status={trade.orderStatus.status})')
            return
        logger.info(trade)
        logger.info('Placed market sell order')
    else:
        logger.info('market order already placed')
        print('market order already placed')
        return 0


def strategy_condition(df,ticker,quantity):
    
    buy_condition=df['ema'].iloc[-1]>df['sma'].iloc[-1] and df['ema'].iloc[-2]<df['sma'].iloc[-2]
    buy_condition=True
    sell_condition=df['ema'].iloc[-1]<df['sma'].iloc[-1] and df['ema'].iloc[-2]>df['sma'].iloc[-2]

    logger.info(f'checking strategy condition for {ticker}')
    if buy_condition:
        logger.info(f'buy condition satisfied for {ticker}')
        print(f'buy condition satisfied for {ticker}')
        # place buy order here
        trade_buy_stocks(ticker, quantity)
    elif sell_condition:
        logger.info(f'sell condition satisfied for {ticker}')
        print(f'sell condition satisfied for {ticker}')
        # place sell order here to close long position
        trade_sell_stocks(ticker, quantity)
    else:
        logger.info(f'no condition satisfied for {ticker}')
        print(f'no condition satisfied for {ticker}')
        return


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
            strategy_condition(df,ticker,quantity)

            
        elif position_status!=0:
            logger.info('we have some position and current ticker is in position')
            print('we have some position and current ticker is in position')

            if position_status==1:
                logger.info('we have current ticker in position and is long')
                print('we have current ticker in position and is long')
                #check exit condition here and place exit order if condition satisfied
                # exit_condition=df['ema'].iloc[-1]<df['sma'].iloc[-1] and df['ema'].iloc[-2]>df['sma'].iloc[-2]
                exit_condition=True
                if exit_condition:
                    logger.info(f'exit condition satisfied for {ticker}')
                    print(f'exit condition satisfied for {ticker}')
                    #place sell order here
                    close_ticker_postion(ticker)
        
        elif position_status==-1:
            logger.info('we have current ticker in position and is short')
            print('we have current ticker in position and is short')
            #check exit condition here and place exit order if condition satisfied
            exit_condition=df['ema'].iloc[-1]>df['sma'].iloc[-1] and df['ema'].iloc[-2]<df['sma'].iloc[-2]
            if exit_condition:
                logger.info(f'exit condition satisfied for {ticker}')
                print(f'exit condition satisfied for {ticker}')
                #place buy order here to close short position
                close_ticker_postion(ticker)





logger.info('Strategy started')
current_time=dt.now(tz=time_zone)
print(current_time)



start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)
print(start_time)
print(end_time)

logger.info('Checking if start time has been reached')
while start_time>dt.now(tz=time_zone):
    print(dt.now(tz=time_zone))
    ib.sleep(1)

logger.info('Starting the main code')



def main():

    while True:

        if dt.now(tz=time_zone)>end_time:
            logger.info('End time reached, closing all positions and stopping the strategy')
            print('End time reached, closing all positions and stopping the strategy')
            #close all positions here
            for ticker in tickers:
                close_ticker_postion(ticker)
            logger.info('End time reached, stopping the strategy')
            print('End time reached, stopping the strategy')
            break
        ct= dt.now(tz=time_zone)
        print(ct)
        #run every 5 min
        # if ct.second==1 and ct.minute%5==0:
        if ct.second==1:
            print('new candle started')
            main_strategy_code()
        time.sleep(1)

main()
print('strtegy ended')