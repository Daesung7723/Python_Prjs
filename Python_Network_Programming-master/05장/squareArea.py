def squareArea(s) :
    area = s * s
    return area   # area 값이 반환됨

a = squareArea(5) # 인자 5를 함수에 전달. 함수의 반환값이 a에 저장
b = squareArea(7) # 인자 7를 함수에 전달. 함수의 반환값이 b에 저장
print("한변의 길이가 %d인 정사각형의 넓이는 %d" %(5, a))
print("한변의 길이가 %d인 정사각형의 넓이는 %d" %(7, b))
