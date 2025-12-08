#dictionary,set

stock_prices={'tsla':400,'goog':900,'reliance':500,'nifty':1000}

#access
print(stock_prices['tsla'])

print(stock_prices.get('tsa',0))

#update

stock_prices['goog']=930

stock_prices.update({'goog':930})
print(stock_prices)

#add a new element 
stock_prices.update({'meta':780})
print(stock_prices)

#remove
stock_prices.pop('nifty')
print(stock_prices)

# del stock_prices['nifty']

#keys,values,items

#sets
s1={3,4,5,5}
s2=set([3,4,5,4])

print(s1)
print(s2)

print(s1.add(70))
print(s1)

#list,str,dictionary