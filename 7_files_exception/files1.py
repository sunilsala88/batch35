

# data='tsla=200'

# f1=open('prices.txt','w')
# f1.write(data)
# f1.close()

# f2=open(r'/Users/algo trading 2026/batch35/7_files_exception/data2.txt','r')
# d=f2.read()
# print(d)
# f2.close()


# data='\nnifty=900'

# f1=open('prices.txt','a')
# f1.write(data)
# f1.close()




stock_price={'amzn':400,'tsla':489,'nifty':389,'goog':890}

def print_stocks():
    for name,price in stock_price.items():
        print(name,':',price)

def take_input():
    protfolio={}
    name=''
    while True:
        name=input('enter the name of stock(q to exit)')
        
        if name=='tsla':
            print('you cannot trade this right now try something else')
            continue



        if name.lower()=='q':
            break

        found=stock_price.get(name)
        if found:
            protfolio.update({name:found})
        else:
            print('unable to find the stock name type again')
    return (protfolio)


def save_data(portfolio:dict)->None:
    f1=open('stock_data.txt','+a')
    for name,price in portfolio.items():
        d=name+':'+str(price)+'\n'
        f1.write(d)
    f1.close()

print_stocks()
port=take_input()
save_data(port)