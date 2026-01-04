

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
        self.id=id
        self.wallet=balance
        self.portfolio={}

    
    def get_port(self):
        for i,j in self.portfolio():
            print(i,j)
    
    def buy(self,name):
        pass

    def sell(self,name):
        pass
