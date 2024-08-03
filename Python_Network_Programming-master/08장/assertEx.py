# assertEx.py
def isEven(n):
    if n % 2 == 0:
        print(n, "is even")
        return True
    else:
        return False

assert isEven(8)
assert isEven(7)
