#GUI_socket_client_class.py
'''
GUI program to send a message and receive it again from server
GUI_socket_client.py
'''

from tkinter import *
from socket import *
import threading
import struct

class TempApp:
    def __init__(self, root, sock):
        self.root = root
        self.sock = sock
        
        self.root.title("Convert Cent to Ferh")
        self.message_label = Label(self.root, text='Enter a temperature(C)  ',font=('Verdana', 16))
        self.entry1 = Entry(self.root, font=('Verdana', 16), width=5)
        self.recv_label = Label(self.root, text='Temperature in F  ',font=('Verdana', 16))
        self.entry2 = Entry(self.root, font=('Verdana', 16), width=5)
        self.calc_button = Button(self.root, text='전송', font=('Verdana', 12), command=self.calculate)

        self.message_label.grid(row=0, column=0, sticky=W)
        self.recv_label.grid(row=1, column=0, sticky=W)
        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)
        self.calc_button.grid(row=0, column=2, padx=10, pady=10)
    
    def calculate(self):
        temp = float(self.entry1.get()) #Read a temp
        #entry1.delete(0,END)도 #입력 창을 지운다
        self.sock.send(str(temp).encode()) #send the temp in C to server

    def handler(self):
        while True:
            r_msg = self.sock.recv(1024) #메시지 수신
            self.entry2.insert(0, struct.unpack('f',r_msg)) #수신 메시지를 박스에 쓴다

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("localhost", 2500))

root = Tk()
MyApp = TempApp(root, sock)

cThread = threading.Thread(target=MyApp.handler, args=())
cThread.daemon = True
cThread.start()

root.mainloop()
