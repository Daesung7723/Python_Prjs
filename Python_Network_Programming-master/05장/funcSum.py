def sum(n):      # 매개변수 n을 전달받는다
    sum = 0
    for i in range(1, n+1): # 1~n까지 반복
        sum = sum + i      # 합에 새로운 수를 더한다
    return sum    # 합을 반환

a = sum(50)
b = sum(1000)
print(a)
print(b)
