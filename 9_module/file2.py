
price=100
name='amzn'

def get_current_price():
    return 101



class Circle:
    pi=3.14

    def __init__(self,r):
        self.radius=r

    def __repr__(self):
        return str( self.radius)
    
    def get_radius(self):
        return self.radius
    
    def circumference(self):
        return 2*self.pi*self.radius
    
    def area(self):
        return 2*self.pi*(self.radius**2)

