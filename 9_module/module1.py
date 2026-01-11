

#module/library/package

import file2
import file2 as f1
import demo.sample1 as t1
import alskdjflkajsdflkajdflkajdlfk as a1
print(a1.a)

print(file2.name)
print(f1.name)
print(file2.price)
print(file2.get_current_price())

c1=file2.Circle(10)
print(c1)

print(t1.free)

from file3 import a1,b2,Order
from file3 import *
print(a1)

import random
import time
print(random.randint(1000,2000))