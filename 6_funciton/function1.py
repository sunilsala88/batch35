
prices=[200,400,500,800]

total=0
for i in prices:
    total=total+i
avg=total/len(prices)
print(avg)

def average(numbers:list)-> float:
    """
    this is a average function which takes list as input and gives float a output
    """
    total=0
    for i in numbers:
        total=total+i
    avg=total/len(numbers)
    return (avg)

a=average(prices)
print(a)


def get_even_numbers(num:int)->list:
    """
    it return n even number
    """
    even=[]
    for i in range(num*2):
        if i%2==0:
            even.append(i)
    return even

a=get_even_numbers(50)
print(a)

def reverse(s1:str)->str:
    s2=''
    for i in s1:
        s2=i+s2
    return s2

a=reverse('hello')
print(a)

'tsla'.index()