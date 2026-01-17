
import numpy as np
#numpy array
l1=[11,22,33,'55']
print(l1)
np1=np.array(l1,dtype='int')
print(np1)

l2=[1,2,3,4]
np2=np.array(l2,dtype=int)
print(np2)

# print(l1-l2)
print(np1%np2)

# print(l1+3)
print(np1*7)

print(np.ones(10,dtype=int))
print(np.zeros(5,dtype=int))
print(np.arange(10,30,2))
print(np.random.randint(100,200,10))

a=np.arange(9)
print(a)