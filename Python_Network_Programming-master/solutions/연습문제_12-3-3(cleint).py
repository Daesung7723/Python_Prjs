#GUI_socket_UDP_client.py

from tkinter import *
from socket import *
import threading
import time

#섭씨 온도를 서버로 전송
def calculate(): #[전송] 버튼 클릭하면 실행
    global sock, data
    temp = float(entry1.get()) #섭씨 온도 읽기
    sock.sendto(str(temp).encode(), ("localhost", 2500)) #섭씨 온도를 서버로 전송

#Thread handler
def handler(conn):
    while 1:
        try: #상대방이 송신하지 않으면 예외 발생
            data, addr = conn.recvfrom(1024)
        except Exception as e: #예외가 발생하면 무시하고 진행
            pass
        else: #수신 데이터 표시
            entry2.delete(0, END) #화씨 온도창을 지운다
            entry2.insert(0, data.decode()) #수신 데이터 표시
            entry1.delete(0, END) #섭씨 입력 창을 지운다
        
if __name__ == '__main__':
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setblocking(True)
    
    root = Tk()
    message_label = Label(text='Enter a temperature(C)  ',font=('Verdana', 16))
    entry1 = Entry(font=('Verdana', 16), width=5)
    
    recv_label = Label(text='Temperature in F ',font=('Verdana', 16))
    entry2 = Entry(font=('Verdana', 16), width=5)
    
    calc_button = Button(text='전송', font=('Verdana', 12), command=calculate)
    
    message_label.grid(row=0, column=0, sticky=W)
    recv_label.grid(row=1, column=0, sticky=W)
    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    calc_button.grid(row=0, column=2, padx=10, pady=10)
    
    # Create a thread to run handler
    cThread = threading.Thread(target=handler, args=(sock,))
    cThread.daemon = True
    cThread.start()
    
    mainloop()
