
# 4 data type int,float,bool,str
#4 more data type today
#data structure (collection of data)
#datastructure ,datatype 
#list,dictionary,tuple,set

l1=[10,20,30,40,50,'jkl'] #list
print(type(l1))
print(l1)

#indexing
print(l1[0],l1[-1])

#slicing
print(l1[0:2])

#update
l1[-1]=60
print(l1)

#add
l1.append(70)
print(l1)

l1.insert(1,15)
print(l1)

#delete
l1.remove(15)
print(l1)

l1.pop(1)
print(l1)

del l1[-1]
print(l1)