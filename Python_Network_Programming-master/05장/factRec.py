def factorial(n):
    if n == 0:
        return 1 # 재귀 함수 종료 조건. n=0이면 종료
    else:
        return n * factorial(n-1) # n! = n x (n-1)! 

print(factorial(5))
