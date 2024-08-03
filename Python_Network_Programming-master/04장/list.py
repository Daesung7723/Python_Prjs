#list.py
cars = ['taxi', 'sedan', 'bus', 'truck']
cars.sort()  # 리스트 요소 변경
print(cars)

cars.sort(reverse=True)
print(cars)

print("Here is the original list:")
print(cars)
print("\nHere is the sorted list:")
print(sorted(cars))  # 원래 리스트는 유지
print("\nHere is the original list again:")
print(cars)
