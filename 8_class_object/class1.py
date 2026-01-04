

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
