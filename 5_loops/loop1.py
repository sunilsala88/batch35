
#looping/iterating(iteration)

# l1=[22,33,44,4,24]
# total=0
# #type 1
# for i in l1:
#     print(i)
#     total=total+i
# print(total)
# avg=total/len(l1)
# print(avg)

l1=[22,33,44,4,24]
total=0
count=0
#type 1
for i in l1:
    print(i)
    total=total+i
    count=count+1
print(total)
avg=total/count
print(avg)

avg=sum(l1)/len(l1)
print(avg)

#type 2 (run a piece of code for n number of times)


print(list(range(10)))
print(list(range(10,20)))
print(list(range(10,20,3)))

for i in range(10):
    print('hello world')

#sum all number from 1 to 100


#type 3 go through the list buy by using index

l1=['Goog','amzn','tsla','ongc']

for i in range(len(l1)):
    print(l1[i])

