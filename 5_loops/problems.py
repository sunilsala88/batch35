


l2=[22,33,44,55]
s2='tsla'

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