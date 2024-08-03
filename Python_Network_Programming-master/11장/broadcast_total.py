# UDP 브로드캐스팅 프로그램

import argparse, socket
BUFSIZE = 1024

def client(network, port): #클라이언트
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = '브로드캐스팅 메시지'
    sock.sendto(text.encode(), (network, port))

def server(interface, port): #서버
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('{}에서 수신 대기 중'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode()
        print('클라이언트({})의 브로드캐스팅 메시지: {!r}'.format(address, text))

if __name__ == '__main__':
    role = {'client': client, 'server': server}
    
    #명령인수 처리
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=role)
    parser.add_argument('host')
    parser.add_argument('-p', type=int, default=1060)
    args = parser.parse_args()
    
    function = role[args.mode] #모드 선택
    function(args.host, args.p) #함수 호출