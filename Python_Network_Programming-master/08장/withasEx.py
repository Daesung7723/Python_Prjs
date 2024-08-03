#withasEx.py
with open('testFile.txt', 'r') as file:
    str = file.read()
    print(str)
    file.close() # with ~ as를 사용하면 이 문장 없어도 됨
