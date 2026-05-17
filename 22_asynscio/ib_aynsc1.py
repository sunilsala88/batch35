
from ib_async import *

util.startLoop()

ib = IB()
ib.connect("127.0.0.1", 7497, clientId=14)



# contract = Stock("GOOG", "SMART", "USD")
contract=Crypto("BTC", "PAXOS", "USD")
# b=ib.qualifyContracts(contract)
# contract=b[0]
# print(contract)
async def get_contract():
    b = await ib.qualifyContractsAsync(contract)
    print(b[0])
import asyncio
asyncio.run(get_contract())


# bars = ib.reqHistoricalData(
#     contract,
#     endDateTime="",
#     durationStr="5 D",
#     barSizeSetting="1 min",
#     whatToShow="MIDPOINT",
#     useRTH=True,
#     formatDate=1,
# )
# bars


# df = util.df(bars)
# df