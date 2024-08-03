# pybluez를 이용한 블루투스 클라이언트 프로그램

import bluetooth

serverMACAddress = "50:77:05:B4:C4:8D" #Galaxy Note 8

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((serverMACAddress, port))

while True:
    text = input("message: ")
    if text == "quit":
        break
    sock.send(text)

sock.close()
