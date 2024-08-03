class People :
    def __init__(self, age=0, name=None):
        self.__age = age
        self.__name = name

    def introMe(self):
        print("Name :", self.__name, "age :", str(self.__age))

class Teacher(People) :
    def __init__(self, age=0, name=None, school=None) :
        super().__init__(age, name) # 매개변수에 self 없음에 주의
        self.__school = school

    def introMe(self):
        super().introMe()
        print("School : ", self.__school)

class Student(Teacher) :
    def __init__(self, age=0, name=None, school=None, grade=None) :
        super().__init__(age, name, school) # 매개변수에 self 없음에 주의
        self.__grade = grade

    def introMe(self):
        super().introMe()
        print("Grade : ", self.__grade)
    
p1 = People(29, "Lee")            # People 객체
p1.introMe()

t1 = Teacher(48, "Kim", "HighSchool")   # Teacher 객체
t1.introMe()

s1 = Student(17, "Park", "HighSchool", 2)
s1.introMe()
