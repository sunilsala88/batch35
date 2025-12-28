


def fibonacci(num:int)->list:
    fib=[0,1]
    num1=fib[0]
    num2=fib[1]

    count=2

    while True:
        if count==num:
            break
        num3=num1+num2
        fib.append(num3)
        num1=num2
        num2=num3
        count=count+1
    return fib

l=fibonacci(100)
print(l)