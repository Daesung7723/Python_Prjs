# pybluez를 이용한 블루투스 서버 프로그램

import bluetooth

#블루투스 소켓 생성
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
 
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
 
client,addr = server_socket.accept()

while True:
    print(client.recv(1024))

client.close()