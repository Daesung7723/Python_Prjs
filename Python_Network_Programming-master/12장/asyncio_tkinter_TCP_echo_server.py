# asyncio event loop과 tkinter event loop를
# 사용한 TCP 에코 서버 프로그램

import asyncio
import threading
import tkinter as tk

def main():
    root = tk.Tk()
    loop = asyncio.get_event_loop()
    Echoserver(root, loop)
    root.mainloop()
    
class Echoserver(asyncio.Protocol):

    def __init__(self, root, event_loop):
        self.lbl_var = tk.StringVar() #엔트리 문자열
        
        root.title("Tk Asyncio Demo")
        tk.Label(root, text="Incoming Message. TCP Port 2500:").pack()
        tk.Entry(root, textvariable=self.lbl_var).pack(fill=tk.X, expand=1)
        
        self.transport = None #나중에 정의될 변수
        self.loop = event_loop
    
        async def connect(): #서버 생성과 연결
            try:
                loop = asyncio.get_running_loop()
            except:
                loop = asyncio.new_event_loop()
            svr = await loop.create_server(lambda: self, '', 2500) #Main()
            async with svr:
                await svr.serve_forever()
            
        def run():
            #loop = asyncio.get_event_loop()
            asyncio.run(connect())
            
        th = threading.Thread(target = run, args=()) #소켓 동작은 스레드로 처리
        th.daemon = True
        th.start()
        
    '''
    프로토콜 클래스 콜백 함수
    '''
    def connection_made(self, transport):
        self.transport = transport
        print(f"{transport.get_extra_info('peername')}와 연결되었습니다")
        
    def connection_lost(self, exc):
        print("연결이 종료되었습니다", exc)
        
    def eof_received(self):
        print("EOF 수신됨")
        
    def data_received(self, data):
        msg = data.decode()
        print("수신 데이터", msg.strip())
        self.transport.write(f"({msg})".encode())
        
        self.lbl_var.set(msg.strip())
        
if __name__ == "__main__":
    main()