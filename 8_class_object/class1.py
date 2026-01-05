

#class
#blueprint of object
#object
#instance of class

#pass
#attribute var inside a class
#class attribute
#object/instance attribute

#method
#__init__ constructor
#constructor is the first method which is executed when you crate a object


stock_name='tsla'

class book:
    book_type='paper'
    book_genre='technical'

    def __init__(self,name,author,price):
        self.name=name
        self.author=author
        self.price=price
        

    def get_price(self):
        return self.price



b1=book('option pricing','john hull',2000)
p=b1.get_price()
print(p)

b2=book('basics of statistics','james',1000)
p=b2.get_price()
print(p)


class Bank:
    bank_name='jpmorgan'

    def __init__(self,name,no,balance):
        self.name=name
        self.id=no
        self.balance=balance
    
    def get_balance(self):
        return self.balance
    
    def deposit(self,money):
        self.balance=self.balance+money
        return self.balance
    
    def withdraw(self,money):
        self.balance=self.balance-money
        return self.balance
    
a1=Bank('sunil',450,2000)
print(a1.get_balance())
balance=a1.deposit(100)
print(balance)

balance=a1.withdraw(500)
print(balance)


class Broker:
    broker_name='ibk'
    stock_prices={'tsla':100,'amzn':500,'nifty':700,'ongc':6000}

    def __init__(self,name,no,balance):
        self.name=name
        self.id=no
        self.wallet=balance
        self.portfolio={}

    def __repr__(self):
        return self.name

    
    def get_port(self):
        print('----------')
        if self.portfolio:
            for i,j in self.portfolio.items():
                print(i,j)
  
    def buy(self,name):
        found=self.stock_prices.get(name)
        if found:
            if self.wallet>found:
                self.portfolio.update({name:found})
                self.wallet=self.wallet-found
            else:
                print('you dont have enough money to buy')
        else:
            print('unable to buy this stock')

    def sell(self,name):
        found=self.portfolio.get(name)
        if found:
            
                self.portfolio.pop(name)
                self.wallet=self.wallet+found
           
        else:
            print('unable to buy this stock')


u1=Broker('sunil',340,1000)
u1.get_port()
u1.buy('tsla')
u1.get_port()
u1.buy('amzn')
u1.get_port()

u1.sell('tsla')
u1.get_port()
print(u1)