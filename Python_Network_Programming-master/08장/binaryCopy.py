inFp, outFp = None, None 
inStr = ""

inFp = open("./test.jpg", "rb")
outFp = open("./testCopied.jpg", "wb")

while True :
    inStr = inFp.read(1)
    if not inStr :
       break
    outFp.write(inStr)

inFp.close()
outFp.close()
print("image file copied.")
