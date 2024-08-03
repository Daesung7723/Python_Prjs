# GUI 채팅 클라이언트
# 서버 주소와 포트 번호를 입력하고 [연결] 버튼을 클릭한다
# 송신창에 메시지를 입력하고 [전송] 버튼을 클릭한다

from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *

class ChatClient:
    client_socket = None
    
    def __init__(self):
        self.initialize_gui()
        
    def initialize_socket(self):
        '''
        TCP socket을 생성하고 server에게 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.ip = self.ip_widget.get().strip()
        self.port = int(self.port_widget.get())

        result = self.client_socket.connect((self.ip, self.port))
        print("connection: ", result)
        self.listen_thread()
        
    def send_chat(self):
        '''
        message를 전송하는 callback 함수
        '''
        senders_name = self.name_widget.get().strip() + ":"
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end',
                        message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
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
        self.ip_label = Label(fr[0], text='서버주소')
        self.port_label = Label(fr[0], text='포트 번호')
        self.conn_btn = Button(fr[0], text = "연결", command = self.initialize_socket) #연결 버튼
        
        self.recv_label = Label(fr[1], text = '수신 메시지:')
        self.chat_transcript_area = ScrolledText(fr[2], height =20, width=60)
        
        self.send_label = Label(fr[3], text = '송신 메시지:')
        self.send_btn = Button(fr[3], text='전송', command=self.send_chat)
        
        self.enter_text_widget = ScrolledText(fr[4], height =5, width=60)
        
        self.name_widget = Entry(fr[0], width =10)
        self.ip_widget = Entry(fr[0], width =14) #서버 주소 입력창
        self.port_widget = Entry(fr[0], width =5) # 포트 번호 입력창
      
        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.ip_label.pack(side=LEFT)
        self.ip_widget.pack(side=LEFT)
        self.port_label.pack(side=LEFT)
        self.port_widget.pack(side=LEFT)
        self.conn_btn.pack(side=LEFT)
        
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
        
    def receive_message(self, so):
        '''
        Server로부터 message를 수신하고 문서창에 표시한다
        '''
        
        while True:
            buf = so.recv(256)
            if not buf:
                break
            self.chat_transcript_area.insert('end',buf.decode('utf-8') + '\n')
            self.chat_transcript_area.yview(END)
        so.close()
        
        
if __name__ == "__main__":
    ChatClient()
    mainloop()
