
#type 1
l1=[22,33,44]

for i in l1:
    print(i)

#type 2

for i in range(10):
    print('hello world')

#type 3

for i in range(len(l1)):
    print(l1[i])

prices=[200,300,400]
volumes=[2000,4000,5000]
#vwap

l=len(prices)
n=0
d=0
for i in range(l):
    p=prices[i]
    v=volumes[i]
    n=n+p*v
    d=d+v
vwap=n/d
print(vwap)