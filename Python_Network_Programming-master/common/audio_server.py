# This is server code to send video and audio frames over TCP

import socket
import threading, wave, pyaudio, pickle,struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611

def audio_stream():
    server_socket = socket.socket()
    #server_socket.bind((host_ip, (port-1)))
    server_socket.bind(("", (port-1)))

    server_socket.listen(5)
    CHUNK = 1024
    wf = wave.open("g:/파이썬교재/sources/book_codes/3판/common/dongyang.wav", 'rb')
    #wf = wave.open("dongyang.wav", 'rb')
    
    #pa = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
   
    
    #stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
    #                channels=wf.getnchannels()-1, # channels = 1
    #                rate=wf.getframerate(),
    #                input=True,
    #                frames_per_buffer=CHUNK)
    
    client_socket,addr = server_socket.accept()
 
    data = None
    while True:
        if client_socket:
            while True:
              
                data = wf.readframes(CHUNK)
                #print(type(data))
                if not data: break
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
            client_socket.close()
                
#t1 = threading.Thread(target=audio_stream, args=())
#t1.start()
audio_stream()