# 메시지를 구독하여 Entry 창에 표시하는 GUI 프로그램

import paho.mqtt.subscribe as subscribe
import threading
from tkinter import *

#메시지를 Entry 창에 표시하는 함수
def Receiving():
    topics = 'control/msg'
    broker = "test.mosquitto.org"
    while True:
        m=subscribe.simple(topics, hostname=broker, msg_count=1)
        entry.delete(0, END)
        entry.insert(1, m.payload.decode('utf-8'))

#1초 마다 Entry 창 갱신
#def polling():
#    Receiving()
#    root.after(1000, polling) #1초 마다 다시 호출

root = Tk()
label1 = Label(root, font=('Verdana', 12), text="수신 메시지")
label1.grid(row=0, column=0)
entry = Entry(font=('Verdana', 10), width=20)
entry.grid(row=0, column=1)

#polling()
th = threading.Thread(target=Receiving, args=())
th.start()

root.mainloop()