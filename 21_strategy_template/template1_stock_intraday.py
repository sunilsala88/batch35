
import datetime

from  ib_async import *
import pendulum as dt
import time
import logging
import pandas as pd
import threading
import requests
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
handler.setFormatter(PendulumFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(PendulumFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

logger.info(f"Current time: {dt.now(time_zone)} - Strategy started")




tickers = ['RELIANCE','AXISBANK','HDFCBANK','KOTAKBANK']
exchange='NSE'
currency='INR'
account_no='DU6327991'
ord_validity='DAY'
quantity_=1

start_hour,start_min=19,2
end_hour,end_min=19,15


contract_objects={}
for ticker in tickers:
    c=ib.qualifyContracts(Stock(ticker,exchange, currency))[0]
    print(c)
    contract_objects[ticker]=c
print(contract_objects)



_order_lock = threading.Lock()
last_run_minute = -1

try:
    order_filled_dataframe=pd.read_csv('order_filled_list.csv')
    order_filled_dataframe.set_index('time',inplace=True)

except Exception:
    column_names = ['time','ticker','price','action']
    order_filled_dataframe = pd.DataFrame(columns=column_names)
    order_filled_dataframe.set_index('time',inplace=True)

TOKEN = ''
ids = ''





def order_open_handler(order):
    global order_filled_dataframe
    if order.orderStatus.status=='Filled':
        try:
            name=order.contract.localSymbol
            action=order.order.action
            price=order.orderStatus.avgFillPrice
            logger.info(f'ORDER FILLED | {name} | {action} | price={price}')
            a=[name, str(price), action]
            fill_time = order.fills[0].execution.time if order.fills else dt.now(time_zone).isoformat()
            with _order_lock:
                order_filled_dataframe.loc[fill_time] = a
                order_filled_dataframe.to_csv('order_filled_list.csv')
            try:
                message='-'.join(a)
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ids}&parse_mode=Markdown&text={message}"
                requests.get(url, timeout=5).json()
                logger.info(f'Telegram notification sent for {name} {action}')
            except Exception:
                logger.exception('Telegram notification failed')
        except Exception:
            logger.exception('Error in order_open_handler')



def close_ticker_position(name):
    # Guard: do not place another close if a market order is already pending
    if not no_pending_market_order(name):
        logger.info(f'Close order already pending for {name}, skipping')
        return
    try:
        pos=ib.positions(account=account_no)
        if not pos:
            logger.info(f'No positions found when trying to close {name}')
            return
        df2=util.df(pos)
        df2['ticker_name']=[cont.symbol for cont in df2['contract']]
        cont=contract_objects[name]
        filtered=df2[df2['ticker_name']==name]
        if filtered.empty:
            logger.info(f'No open position found for {name}, skipping close')
            return
        quant=filtered.position.iloc[0]
        logger.info(f'Closing position | {name} | qty={quant}')
        trade=None
        if quant>0:
            try:
                ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=abs(quant),action='SELL',account=account_no,tif=ord_validity)
                trade=ib.placeOrder(cont,ord)
                logger.info(f'Close SELL order placed | {name} | qty={abs(quant)}')
            except Exception:
                logger.exception(f'Failed to place SELL close order for {name}')
        elif quant<0:
            try:
                ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=abs(quant),action='BUY',account=account_no,tif=ord_validity)
                trade=ib.placeOrder(cont,ord)
                logger.info(f'Close BUY order placed | {name} | qty={abs(quant)}')
            except Exception:
                logger.exception(f'Failed to place BUY close order for {name}')
        # Wait for close order to fill
        if trade is not None:
            elapsed=0
            while trade.orderStatus.status not in ('Filled','ApiCancelled','Cancelled') and elapsed<15:
                ib.sleep(1)
                elapsed+=1
            if trade.orderStatus.status=='Filled':
                logger.info(f'Close order filled | {name} | fill_price={trade.orderStatus.avgFillPrice}')
            else:
                logger.error(f'Close order NOT filled within timeout | {name} | status={trade.orderStatus.status}')
    except Exception:
        logger.exception(f'Unexpected error in close_ticker_position for {name}')

def get_historical_data(ticker_contract,bar_size,duration):
    logger.info(f'Fetching historical data | {ticker_contract.symbol} | {bar_size} | {duration}')
    try:
        bars = ib.reqHistoricalData(
        ticker_contract, endDateTime='', durationStr=duration,
        barSizeSetting=bar_size, whatToShow='TRADES', useRTH=True,formatDate=1)
    except Exception:
        logger.exception(f'Exception fetching historical data for {ticker_contract.symbol}')
        return None
    if not bars:
        logger.error(f'No historical data returned for {ticker_contract.symbol}')
        return None
    # convert to pandas dataframe:
    df = util.df(bars)
    if df is None or df.empty or len(df) < 21:
        logger.error(f'Insufficient historical data for {ticker_contract.symbol} (rows={0 if df is None else len(df)})')
        return None
    df['ema']=df['close'].ewm(span=10).mean()
    df['sma']=df['close'].rolling(window=20).mean()
    df.dropna(subset=['ema','sma'],inplace=True)
    if df.empty or len(df)<2:
        logger.error(f'Not enough rows after dropping NaN for {ticker_contract.symbol}')
        return None
    logger.info(f'Indicators ready | {ticker_contract.symbol} | rows={len(df)} | last_close={df["close"].iloc[-1]:.2f} | ema={df["ema"].iloc[-1]:.2f} | sma={df["sma"].iloc[-1]:.2f}')
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

def no_pending_market_order(name):
    """Return True if there is NO pending market order for this ticker, False if one exists."""
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
    if no_pending_market_order(stock_name):
        try:
            ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=quantity,action='BUY',account=account_no,tif=ord_validity)
            trade=ib.placeOrder(contract,ord)
            logger.info(f'BUY order submitted | {stock_name} | qty={quantity}')
            elapsed=0
            while trade.orderStatus.status not in ('Filled','ApiCancelled','Cancelled') and elapsed<15:
                ib.sleep(1)
                elapsed+=1
            if trade.orderStatus.status != 'Filled':
                logger.error(f'BUY order not filled within timeout | {stock_name} | status={trade.orderStatus.status}')
                return
            logger.info(f'BUY order filled | {stock_name} | qty={quantity} | fill_price={trade.orderStatus.avgFillPrice}')
        except Exception:
            logger.exception(f'Exception placing BUY order for {stock_name}')
    else:
        logger.info(f'BUY skipped — market order already pending for {stock_name}')
        return 0

def trade_sell_stocks(stock_name, quantity):
    contract = contract_objects[stock_name]
    if no_pending_market_order(stock_name):
        try:
            ord=Order(orderId=ib.client.getReqId(),orderType='MKT',totalQuantity=quantity,action='SELL',account=account_no,tif=ord_validity)
            trade=ib.placeOrder(contract,ord)
            logger.info(f'SELL order submitted | {stock_name} | qty={quantity}')
            elapsed=0
            while trade.orderStatus.status not in ('Filled','ApiCancelled','Cancelled') and elapsed<15:
                ib.sleep(1)
                elapsed+=1
            if trade.orderStatus.status != 'Filled':
                logger.error(f'SELL order not filled within timeout | {stock_name} | status={trade.orderStatus.status}')
                return
            logger.info(f'SELL order filled | {stock_name} | qty={quantity} | fill_price={trade.orderStatus.avgFillPrice}')
        except Exception:
            logger.exception(f'Exception placing SELL order for {stock_name}')
    else:
        logger.info(f'SELL skipped — market order already pending for {stock_name}')
        return 0


def strategy_condition(df,ticker,quantity):
    ema_now=df['ema'].iloc[-1]
    sma_now=df['sma'].iloc[-1]
    ema_prev=df['ema'].iloc[-2]
    sma_prev=df['sma'].iloc[-2]
    buy_condition=ema_now>sma_now and ema_prev<sma_prev

    logger.info(f'Checking entry condition | {ticker} | ema={ema_now:.2f} sma={sma_now:.2f} | prev_ema={ema_prev:.2f} prev_sma={sma_prev:.2f}')
    if buy_condition:
        logger.info(f'BUY entry condition satisfied | {ticker} | qty={quantity}')
        trade_buy_stocks(ticker, quantity)
    else:
        # sell_condition when flat would open a naked short — skipped intentionally
        logger.info(f'No entry condition satisfied | {ticker}')
        return


def main_strategy_code():
    logger.info(f'========== main_strategy_code called | {dt.now(tz=time_zone)} ==========')

    ord=ib.openOrders()
    print(ord)

    for ticker in tickers:
        try:
            # Refresh capital and positions each iteration so orders placed earlier are reflected
            pos=ib.positions(account=account_no)
            funds_list = [v for v in ib.accountValues(account=account_no) if v.tag == 'AvailableFunds']
            if not funds_list:
                logger.error(f'Could not retrieve AvailableFunds, skipping {ticker}')
                continue
            capital=int(float(funds_list[0].value))
            per_ticker_capital=capital/len(tickers)
            c=contract_objects[ticker]
            df=get_historical_data(c,'1 min','3 D')
            if df is None:
                logger.error(f'Skipping {ticker} due to missing historical data')
                continue
            current_price=df['close'].iloc[-1]
            quantity=int(per_ticker_capital/current_price)
            position_status=get_info_about_position(pos,ticker)
            logger.info(f'--- {ticker} | price={current_price:.2f} | capital={capital} | qty={quantity} | position={position_status} ---')

            if quantity==0:
                logger.info(f'Insufficient capital to trade {ticker}, skipping')
                continue

            if position_status==0:
                logger.info(f'No position in {ticker}, checking entry')
                strategy_condition(df,ticker,quantity)

            elif position_status==1:
                logger.info(f'Long position in {ticker}, checking exit')
                exit_condition=df['ema'].iloc[-1]<df['sma'].iloc[-1] and df['ema'].iloc[-2]>df['sma'].iloc[-2]
                if exit_condition:
                    logger.info(f'EXIT condition satisfied for long {ticker}')
                    close_ticker_position(ticker)
                else:
                    logger.info(f'No exit condition for long {ticker}')

            elif position_status==-1:
                logger.info(f'Short position in {ticker}, checking exit')
                exit_condition=df['ema'].iloc[-1]>df['sma'].iloc[-1] and df['ema'].iloc[-2]<df['sma'].iloc[-2]
                if exit_condition:
                    logger.info(f'EXIT condition satisfied for short {ticker}')
                    close_ticker_position(ticker)
                else:
                    logger.info(f'No exit condition for short {ticker}')

        except Exception:
            logger.exception(f'Unexpected error processing {ticker}, skipping')
            continue





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

ib.orderStatusEvent += order_open_handler

def main():
    global last_run_minute
    while True:
        try:
            if dt.now(tz=time_zone)>end_time:
                logger.info('End time reached — closing all positions and stopping strategy')
                for ticker in tickers:
                    try:
                        close_ticker_position(ticker)
                    except Exception:
                        logger.exception(f'Error closing position for {ticker} at end of day')
                # Verify all positions are actually closed
                ib.sleep(2)
                remaining_pos=ib.positions(account=account_no)
                if remaining_pos:
                    remaining_df=util.df(remaining_pos)
                    remaining_df['ticker_name']=[cont.symbol for cont in remaining_df['contract']]
                    for ticker in tickers:
                        r=remaining_df[remaining_df['ticker_name']==ticker]
                        if not r.empty and r.position.iloc[0]!=0:
                            logger.error(f'POSITION STILL OPEN after EOD close attempt | {ticker} | qty={r.position.iloc[0]} — retrying')
                            try:
                                close_ticker_position(ticker)
                            except Exception:
                                logger.exception(f'Retry close failed for {ticker}')
                logger.info('All positions closed. Strategy stopped.')
                break
            ct= dt.now(tz=time_zone)
            #run every 5 min
            # if ct.second==1 and ct.minute%5==0:
            if ct.second<=3 and ct.minute!=last_run_minute:
                last_run_minute=ct.minute
                logger.info(f'New candle | {ct}')
                main_strategy_code()
            ib.sleep(1)  # use ib.sleep so the event loop processes order/fill updates
        except Exception:
            logger.exception('Unexpected error in main loop — continuing')
            ib.sleep(1)

main()
print('strategy ended')