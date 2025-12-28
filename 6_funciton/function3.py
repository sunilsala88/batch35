def greet_user(name, age):
    print(f"Hello {name}, you are {age} years old.")

#positional argument
greet_user("Alice", 25)
greet_user( 25,'Alice')


#keyword argument

greet_user(name="Alice", age=25)
greet_user( age=25,name='Alice')

#default argument

def greet(name="User"):
    print("Hello", name)

greet()       # Uses default
greet("Niel") # Uses passed value

def power(num1,num2=1):
    return num1**num2
a=power(10)
print(a)
# #fstring
# age=10
# name='sam'
# word='my name is '+ name +'my age is '+str(age)
# print(word)

# word1=f"my name is {name} and my age is {age}"
# print(word1)