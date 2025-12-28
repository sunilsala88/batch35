


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

# print_stocks()
# p=take_input()
# print(p)

#is_palindrome input string ,True False

def rev_str(s1):
    s2=''
    for i in s1:
        s2=i+s2
    return s2

def is_palindrome(s1:str)->bool:

    s2=rev_str(s1)  
    print(s2)  
    if s1==s2:
        return True
    else:
        return False

a=is_palindrome('radai')
print(a)


#flow of funtion

def fun1(a,b):
    return a**2+b
def fun2(x,y,z):
    a=fun1(x,y) #3
    a=a+z #6
    return a

def fun3(i,j,k):

    n=fun1(j,k) #7
    m=fun2(i,j,k) #6
    return n+m

t=fun3(1,2,3)
print(t)


