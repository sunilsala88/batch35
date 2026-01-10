



# class Circle:
#     pi=3.14

#     def __init__(self,r):
#         self.radius=r
    
#     def get_radius(self):
#         return self.radius
    
#     def circumference(self):
#         return 2*self.pi*self.radius
    
#     def area(self):
#         return 2*self.pi*(self.radius**2)
    
# l1=[2,5,7,8,9,10]
# for r in l1:
#     print('------')
#     c1=Circle(r)
#     print(c1.radius)
#     print(c1.get_radius())
#     print(c1.circumference())
#     print(c1.area())

        
#101
#100
#99

class Order:

    def __init__(self,name,current_price,sl,tp):
        self.name=name
        self.current_price=current_price
        self.stop_loss=sl
        self.take_profit=tp
        self.fill=False
        self.position=False
        
    
    def palce_order(self):
        print('places market order')
        print('got a fill')
        self.fill=True
        self.fill_price=self.current_price-1
        self.position=True
        self.stop_value=self.fill_price-((self.stop_loss/100)*self.fill_price)
        self.take_profit_value=self.fill_price+((self.take_profit/100)*self.fill_price)
    
    def check_stop_loss(self,price):
        current_stop_loss=self.fill_price-((self.stop_loss/100)*self.fill_price)
        
        if price<current_stop_loss and self.position:
            print('position closed')
            self.position=False

    def check_take_profit(self,price):
        current_take_profit=self.fill_price+((self.take_profit/100)*self.fill_price)
        
        if price>current_take_profit and self.position:
            print('position closed')
            self.position=False


a1=Order('amzn',101,5,5)
a1.palce_order()

l1=[100,100,101,96,94,93,92,100,102,106,110]
for price in l1:
    print(f'current price is {price} and sl {a1.stop_value} is and tp is {a1.take_profit_value}')
    a1.check_stop_loss(price)
    a1.check_take_profit(price)