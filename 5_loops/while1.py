
num=0

while True:
    if num==5:
        break
    print(num)

    num=num+1


# num=0
# while num!=10:
#     print(num)
#     num=num+1


# num=0
# even=[]
# while True:
#     if num==101:
#         break
#     print(num)
#     if num%2==0:
#         even.append(num)

#     num=num+1
# print(even)


stock_price={'amzn':400,'tsla':489,'nifty':389,'goog':890}
protfolio=[]
name=''
while True:
    
    if name=='tsla':
        print('you cannot trade this right now try something else')
        continue

    name=input('enter the name of stock(q to exit)')

    if name.lower()=='q':
        break

    found=stock_price.get(name)
    if found:
        protfolio.append(name)
    else:
        print('unable to find the stock name type again')
print(protfolio)




l2=[22,33,44,55]
s2='tsla'

final=[]
for i in l2:
    final.insert(0,i)
print(final)