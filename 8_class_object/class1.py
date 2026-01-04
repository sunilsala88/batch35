

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


def get_price():
    return 100


class book:
    book_type='paper'
    book_genre='technical'

    def __init__(self,name,author,price):
        self.name=name
        self.author=author
        self.price=price


b1=book('option pricing','john hull',2000)

p=get_price()