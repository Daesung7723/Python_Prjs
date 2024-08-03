#pick 6 from 1-45

import random

pick = set() # 빈 집합
while len(pick) < 6:
    n = random.randint(1,45)
    if n not in pick:
        pick.add(n) # 집합에 요소 추가
print(pick)
print(sorted(pick)) # 숫자 순서대로 출력
