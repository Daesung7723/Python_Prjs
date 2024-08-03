# rpi_select_GUI_client.py

from socket import *
from tkinter import *
import time, threading
from select import *

# data receiving and handling
def handle(sock):
    while True:
        r_sock, w_sock, e_sock = select([sock], [], [], 0)
        if r_sock:
            msg = sock.recv(1024).decode()
            if msg.upper() == 'OFF':
                switch_state_label.configure(text='Switch is OFF')
            else:
                switch_state_label.configure(text='Switch is ON')
            
# button click callback
def button_command():
    global sock, btn_text, btn_color
    if btn_text == 'ON':
        btn_text = 'OFF'
        btn_color = 'blue'
    else:
        btn_text = 'ON'
        btn_color = 'red'
    LED_button.configure(text=btn_text, bg=btn_color)
    sock.send(btn_text.encode())
    
# generate a socket and connect
sock = socket()
sock.connect(('192.168.137.2', 2500))

# Root windows
root = Tk()
btn_color = 'red'
btn_text = 'ON'

LED_label = Label(text="LED")
Switch_label = Label(text="SWITCH")
switch_state_label = Label(text="Switch is OFF",fg='blue')
LED_button = Button(text=btn_text, fg='yellow', bg=btn_color, command=button_command)

LED_label.grid(row=0, column=0)
LED_button.grid(row=0, column=1)
Switch_label.grid(row=1, column=0)
switch_state_label.grid(row=1, column=1, sticky=E)

Cthread = threading.Thread(target=handle, args=(sock, ))
Cthread.daemon = True
Cthread.start()

root.mainloop()
