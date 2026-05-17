#parallel programming->when we have to do some CPU intensive task, we can use parallel programming to utilize multiple CPU cores to run multiple tasks simultaneously. This is especially useful when we have to perform heavy computations, such as data processing, machine learning, etc.
#concurrent programming->when we have to do some tasks that can be executed independently, we can use concurrent programming to run multiple tasks concurrently. This is especially useful when we have to perform tasks that are not dependent on each other, such as handling multiple client requests in a web server, etc.

#asynchronous programming->when we have to do some tasks that are I/O bound, we can use asynchronous programming to run multiple tasks asynchronously. This is especially useful when we have to perform tasks that involve waiting for some I/O operations to complete, such as reading/writing files, making network requests, etc.
#coroutines->coroutines are special functions that can be paused and resumed at a later time. They are defined using the async keyword and can be used to write asynchronous code in a more readable and maintainable way.

#https://www.youtube.com/watch?v=K56nNuBEd0c

# import time
# def fun1():
#     print('fun1 first line')
#     time.sleep(1)
#     print('fun1 ends')

# def fun2():
#     print('fun2 first line')
#     time.sleep(1)
#     print('fun2 ends')

# fun1()
# fun2()




import asyncio
async def fun1():
    print('fun1 first line')
    await asyncio.sleep(1)
    print('fun1 ends')

async def fun2():
    print('fun2 first line')
    await asyncio.sleep(1)
    print('fun2 ends')

async def fun3():
    print('fun3 first line')
    await asyncio.sleep(1)
    print('fun3 ends')


async def main():
    # await fun1()
    # await fun2()
    await asyncio.gather(fun1(),fun2(),fun3())



asyncio.run(main())