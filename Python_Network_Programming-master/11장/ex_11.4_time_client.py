import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5000))
cur_time = s.recv(1024).decode()
print("원형:",cur_time)
parsed_time = cur_time.split()
print("현재 시각: ", parsed_time[4], parsed_time[1], parsed_time[2], "(%s)"%parsed_time[0], parsed_time[3])
