# a에 있는 n개의 원판을 b를 이용해 c로 옮김
def move(n, a, b, c):
    if n > 0:
        move(n-1, a, c, b) # a에 있는 n-1개의 원판을 c를 이용해 b로 옮김
        print("Move a disk from %s to %s" %(a,c))
        move(n-1, b, a, c) # b에 있는 n-1개의 원판을 a를 이용해 c로 옮김

move(3, 'a', 'b', 'c') # a에 있는 3개의 원판을 b를 이용해 c로 옮김
