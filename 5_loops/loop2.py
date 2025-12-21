#type 4

stock_price={'amzn':400,'tsla':489,'nifty':389}

for i in stock_price:
    print(i,stock_price[i])

print(list(stock_price.keys()))
print(list(stock_price.values()))
print(list(stock_price.items()))


#type 4
for i,j in stock_price.items():
    print(i,j)