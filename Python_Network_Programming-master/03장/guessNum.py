#guessNum.py
trial = 5
while trial > 0 :
    number = int(input('Enter any integer number : '))
    if number < 0:
        print('음의 수')
    elif number > 0:
        print('양의 수')
    else:
        print('영(zero)')
    trial = trial - 1
