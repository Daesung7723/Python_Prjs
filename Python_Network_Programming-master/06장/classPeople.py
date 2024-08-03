class People :
    def __init__(self, age=0, name=None):
        self.__age = age
        self.__name = name

    def introMe(self):
        print("Name :", self.__name, "age :", str(self.__age))

class Teacher(People) :
    def __init__(self, age=0, name=None, school=None) :
        super().__init__(age, name) # 부모클래스 호출.  매개변수에 self 없음!
        self.__school = school      # 자신의 인스턴스변수 추가

    def showSchool(self):
        print("My school : ", self.__school)

p1 = People(29, "Lee")   # People 객체 호출
p1.introMe()             # People.introMe() 호출

t1 = Teacher(48, "Kim", "HighSchool")   # Teacher 객체
t1.introMe()                           # People.introMe() 호출
t1.showSchool()           # Teacher.showSchool() 호출
