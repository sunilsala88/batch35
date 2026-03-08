
from ib_async import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=93)


contract1=Crypto('ETH','PAXOS','USD')
contract1=ib.qualifyContracts(contract1)[0]



def abc(t):
    t=list(t)[0]
    print(t.contract.symbol,t.time,t.bid,t.ask)

market_data=ib.reqMktData(contract1, "", False, False)


ib.pendingTickersEvent += abc
# ib.sleep(20)
# ib.pendingTickersEvent -= pending_tick
ib.run()


