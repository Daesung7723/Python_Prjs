#people.py
class People(object) :
    
    def __init__(self, age=0, name=None):
        self.__age = age
        self.__name = name

    def __str__(self):
        return super().__str__()

p1 = People(29, "John")
print(p1)
