#pick 6 from 1-45

import random

pick = set()  # 빈 집합
while True:
    n = random.randint(1,45)
    if n in pick:
        continue
    else:
        pick.add(n)
    if len(pick) == 6:
        break
print(pick)
print(sorted(pick))
