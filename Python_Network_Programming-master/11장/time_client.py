#타임 클라이언트 프로그램

import socket, pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5000))
print("현재 시각: ", sock.recv(1024).decode())

sock.close()
