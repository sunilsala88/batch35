
try:
    print('this is algo trading')
    num1=int(input('enter a num'))
    num2=int(input('enter a num'))
    result=num1/num2
    print(result)
except Exception as e:
    print(e)
    print('something went wrong')

print('this is important last line')