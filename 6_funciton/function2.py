


def fibonacci(num:int)->list:
    global a
    fib=[0,1]
    num1=fib[0]
    num2=fib[1]
    a='amzn'
    print(a)
    count=2
    print(count)
    while True:
        if count==num:
            break
        num3=num1+num2
        fib.append(num3)
        num1=num2
        num2=num3
        count=count+1
    return fib

a='tsla'
l=fibonacci(10)
print(l)
print(a)


stock_price={'amzn':400,'tsla':489,'nifty':389,'goog':890}
protfolio=[]
name=''
while True:
    
    if name=='tsla':
        print('you cannot trade this right now try something else')
        continue

    name=input('enter the name of stock(q to exit)')

    if name.lower()=='q':
        break

    found=stock_price.get(name)
    if found:
        protfolio.append(name)
    else:
        print('unable to find the stock name type again')
print(protfolio)

#print_stocks
#take_input
