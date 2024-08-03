#polymorph.py
class Korean(object):
    def greeting(self):
        print("안녕하세요")

class American(object):
    def greeting(self):
        print("Hello")

def sayhello(people):
    people.greeting()
    
Kim = Korean()
John = American()
sayhello(Kim)
sayhello(John)
