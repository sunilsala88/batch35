
a1=10

b2=3000



class Order:

    def __init__(self,name,current_price,sl,tp):
        self.name=name
        self.current_price=current_price
        self.stop_loss=sl
        self.take_profit=tp
        self.fill=False
        self.position=False
    
    def __repr__(self):
        return self.name+ 'order at '+ str(self.current_price)
    
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
