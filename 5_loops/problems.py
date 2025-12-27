


l2=[22,33,44,55]


final=[]
for i in l2:
    final.insert(0,i)
print(final)

print(list(range(3,-1,-1)))
final2=[]
for i in range(len(l2)-1,-1,-1):
    final2.append(l2[i])

print(final2)

final3=[]
for i in range(-1,-(len(l2)+1),-1):
    final3.append(l2[i])
print(final3)


s2='tsla'

f1=''
for i in s2:
    f1=i+f1
print(f1)

f2=''
#positive index
for i in range(len(s2)-1,-1,-1):
    f2=f2+s2[i]
print(f2)

f3=''
for i in range(-1,-(len(s2)+1),-1):
    f3=f3+s2[i]
print(f3)


#8 table
#8 *1 =8
#8* 2= 16

num=8
for i in range(1,11):
    print(num,' * ',i,'=',num*i)

num=55
data=[44,55,66,77,55,55,67,89]
count=0
for i in data:
    if num==i:
        count=count+1
print(count)