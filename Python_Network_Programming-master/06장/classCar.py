class Car :
    def __init__(self, color, speed) : # 초기화 메소드
        self.color = color         # 인스턴스 변수 정의
        self.speed = speed

    def speedUp(self, v): # 가속 메소드. 1번째 매개변수는 self
        self.speed = self.speed + v
        return self.speed

    def speedDown(self, v): # 감속 메소드
        self.speed = self.speed - v
        return self.speed

c1 = Car('black', 50)
c2 = Car('red', 70)
print('Car c1 : color=%s, speed=%d ' %(c1.color, c1.speed))
print('Car c2 : color=%s, speed=%d ' %(c2.color, c2.speed))
c1.speedDown(10)        # 차 c1의 속도 10만큼 감속
print('Car c1 : speed=%d' %c1.speed)
