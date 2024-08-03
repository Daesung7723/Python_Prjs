import pickle

Pres = { "Kennedy": 35, "Obama": 44}

# 딕셔너리를 피클 파일에 저장
pickle.dump(Pres, open("pres.pic", "wb"))

# 피클 파일에 딕셔너리를 로딩
Pres2 = pickle.load(open("pres.pic", "rb"))
Pres2['Trump'] = 45

pickle.dump(Pres2, open("pres2.pic", "wb"))
print(Pres)
print(Pres2)
