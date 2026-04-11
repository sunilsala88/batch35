
from  ib_async import *
import pendulum as dt
import time
time_zone='UTC'
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



def main_strategy_code():
    print("inside main strategy")
    pos=ib.positions(account=account_no)
    print(pos)




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
        

main()




#function which will run every min
#fetch my postion,check your orders
#check the price of the stock
#check how money we have
#check entry and exit rules
#place order if entry rules are satisfied
#close position if exit rules are satisfied