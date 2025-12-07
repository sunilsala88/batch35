#dictionary,set

stock_prices={'tsla':400,'goog':900,'reliance':500,'nifty':1000}

#access
print(stock_prices['tsla'])

print(stock_prices.get('tsla'))

#update
stock_prices.update({'goog':930})
print(stock_prices)

#add a new element 
stock_prices.update({'meta':780})
print(stock_prices)

#remove
stock_prices.pop('nifty')
print(stock_prices)


#keys,values,items