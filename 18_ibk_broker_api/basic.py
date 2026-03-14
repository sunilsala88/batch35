
# sunil@fessorpro.com
# sunilquant
# quantsunil@123


#https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#bp-alloc-setup

#https://ib-api-reloaded.github.io/ib_async/

#https://github.com/ib-api-reloaded/ib_async



# from ib_async import *
# # util.startLoop()  # uncomment this line when in a notebook

# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=1)

# # Request historical data
# contract = Forex('EURUSD')
# bars = ib.reqHistoricalData(
#     contract, endDateTime='', durationStr='30 D',
#     barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# # Convert to pandas dataframe (pandas needs to be installed):
# df = util.df(bars)
# print(df.head())

# ib.disconnect()


# from ib_async import *

# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=1)

# # Get account summary
# account = ib.managedAccounts()[0]
# summary = ib.accountSummary(account)
# for item in summary:
#     print(f"{item.tag}: {item.value}")

# ib.disconnect()


#https://interactivebrokers.github.io/tws-api/basic_orders.html