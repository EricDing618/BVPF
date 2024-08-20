import os

print('当前路径：',os.getcwd())
def fib(n):    #   递归式斐波那契数列
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1)+fib(n-2)
print(fib(10))    #   打印第10项值