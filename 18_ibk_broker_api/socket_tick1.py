
from ib_async import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=53)

import pendulum
time_zone='UTC'

contract1=Crypto('ETH','PAXOS','USD')
contract1=ib.qualifyContracts(contract1)[0]

contract2=Crypto('BTC','PAXOS','USD')
contract2=ib.qualifyContracts(contract2)[0]


# def abc(t):
#     t=list(t)[0]
#     print(pendulum.now(time_zone), t.contract.symbol, t.lastTimestamp, t.bid, t.ask)

# market_data=ib.reqMktData(contract1, "", False, False)
# market_data=ib.reqMktData(contract2, "", False, False)


# ib.pendingTickersEvent += abc
# # ib.sleep(20)
# # ib.pendingTickersEvent -= abc
# ib.run()




def onBarUpdate(bars, hasNewBar):
    print(util.df(bars))


contract2=Crypto('ETH','PAXOS','USD')
bars = ib.reqRealTimeBars(contract2, 5, 'TRADES', False)
bars.updateEvent += onBarUpdate

# ib.sleep(30)
# bars.updateEvent -= onBarUpdate
# ib.cancelRealTimeBars(bars)
ib.run()



