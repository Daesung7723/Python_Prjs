class Machine:
    sNumber = 0
    def __init__(self):
        Machine.sNumber += 1
        self.number = Machine.sNumber

m1 = Machine()
print(m1.sNumber)
m2 = Machine()
print(m2.sNumber)
