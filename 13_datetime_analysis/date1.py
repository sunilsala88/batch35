


d='2026-01-31'



class samay:
    max_month=12
    max_day=31

    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
        if self.month>12:
            print('invalid month')
        self.month=month
        if day>31:
            print('invalid day')
        self.day=day
    def __repr__(self):
        return f"{self.year}-{self.month}-{self.day}"
    
    def add_day(self,days=1):
        """
        days cannot be greater than 30
        """
        temp=self.day+days
        if temp>self.max_day:
            self.month=self.month+1
        else:
            self.day=self.day+days


d1=samay(2024,1,1)
print(d1)
d1.add_day(31)
print(d1)


        
