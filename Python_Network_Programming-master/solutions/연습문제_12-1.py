from socket import *
import _thread

BUFF = 1024
HOST = ''
PORT = 2500

def handler(clientsock, addr):
    while True:
        data = clientsock.recv(BUFF)
        print('\ndata:' + repr(data))
        if not data: break
        #clientsock.send(response('').encode())
        #print('sent:' + repr(response('')))
        # clientsock.close()
        
def write_handle(clientsock, addr):
    while True:
        s_msg = input('Server message: ')
        clientsock.send(s_msg.encode())

if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while True:
        print('waiting for connection...')
        clientsock, addr = serversock.accept()
        print('...connected from:', addr)
        _thread.start_new_thread(handler, (clientsock, addr))
        _thread.start_new_thread(write_handle, (clientsock, addr))
