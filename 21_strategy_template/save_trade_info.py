import pandas as pd
import datetime 
import time
import threading
from ib_async import *
import pandas as pd
import pandas_ta as ta
import logging
logging.basicConfig(level=logging.INFO, filename=f'super_{datetime.date.today()}',filemode='a',format="%(asctime)s - %(message)s")

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=18)

_order_lock = threading.Lock()

try:
    order_filled_dataframe=pd.read_csv('order_filled_list.csv')
    order_filled_dataframe.set_index('time',inplace=True)

except Exception:
    column_names = ['time','ticker','price','action']
    order_filled_dataframe = pd.DataFrame(columns=column_names)
    order_filled_dataframe.set_index('time',inplace=True)




def order_open_handler(order):
    global order_filled_dataframe
    if order.orderStatus.status=='Filled':
        print('order filled')
        logging.info('order filled')
        name=order.contract.localSymbol
        a=[name,order.orderStatus.avgFillPrice,order.order.action]
        with _order_lock:
            order_filled_dataframe.loc[order.fills[0].execution.time] = a
            order_filled_dataframe.to_csv('order_filled_list.csv')
        message=order.contract.localSymbol+" "+order.order.action+"  "+str(order.orderStatus.avgFillPrice)
        logging.info(message)



ib.orderStatusEvent += order_open_handler

import pendulum as dt
time_zone='America/New_York'
ct= dt.now(time_zone)
while True:
    time.sleep(1)
    print(dt.now(time_zone))
