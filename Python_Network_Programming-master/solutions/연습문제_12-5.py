#UDP_GUI_ChatClient.py
#서버: chatserver_udp.py
'''
GUI 채팅 클라이언트
'''

from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *

class ChatClient:
    client_socket = None
    last_received_message = None
    
    def __init__(self, ip, port):
        self.initialize_socket(ip, port)
        self.initialize_gui() #GUI 화면 구성
        self.listen_thread() #서브 스레드 생성과 시작
        
    def initialize_socket(self, ip, port):
        '''
        UDP socket을 생성
        '''
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.remote_ip = ip
        self.remote_port = port
        self.client_socket.setblocking(True)
        #self.client_socket.connect((self.remote_ip, self.remote_port))
        
    def send_chat(self):
        '''
        message를 전송하는 callback 함수
        '''
        senders_name = self.name_widget.get().strip() + ":"
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end',message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.sendto(message, (self.remote_ip, self.remote_port))
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'        
        
    def initialize_gui(self):
        '''
        위젯을 배치하고 초기화한다
        '''
        self.root = Tk()
        fr = []
        for i in range(0,5):
            fr.append(Frame(self.root))
            fr[i].pack(fill=BOTH)
                
        self.name_label = Label(fr[0], text='사용자 이름')
        self.recv_label = Label(fr[1], text = '수신 메시지:')
        self.send_label = Label(fr[3], text = '송신 메시지:')
        self.send_btn = Button(fr[3], text='전송', command=self.send_chat)
        self.chat_transcript_area = ScrolledText(fr[2], height =20, width=60)
        self.enter_text_widget = ScrolledText(fr[4], height =5, width=60)
        self.name_widget = Entry(fr[0], width =15)
      
        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.recv_label.pack(side=LEFT)
        self.send_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, padx=2, pady=2)
        self.send_label.pack(side=LEFT)
        self.enter_text_widget.pack(side=LEFT, padx=2, pady=2)
        
    def listen_thread(self):
        '''
        Thread를 생성하고 시작한다
        '''
        
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()
        
    def receive_message(self, sock):
        '''
        Server로부터 message를 수신하고 문서창에 표시한다
        '''
        
        while True:
            try:
                msg, addr = sock.recvfrom(1024)
                if not msg:
                    break
                self.chat_transcript_area.insert('end',msg.decode() + '\n')
                self.chat_transcript_area.yview(END)
            except:
                continue
        sock.close()     

        
if __name__ == "__main__":
    ip = input("server IP addr: ")
    if ip == '':
        ip = '127.0.0.1'    
    port = 2500
    ChatClient(ip, port)
    mainloop()
