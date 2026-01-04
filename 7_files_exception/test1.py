

a=open('7_files_exception/data2.txt','r')
d=a.read()
print(d)
a.close()


with open('7_files_exception/data2.txt','r') as a:
    d=a.read()
    print(d)


#iterable
#loopable

f1=open('stock_data.txt','r')

for line in f1:
    print(line)

