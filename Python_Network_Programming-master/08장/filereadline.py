filein = open("./phones1.txt", "r", encoding="utf-8")
readLine = filein.readline().rstrip()
while readLine != "" :
    print(readLine)
    readLine = filein.readline().rstrip()
filein.close()
