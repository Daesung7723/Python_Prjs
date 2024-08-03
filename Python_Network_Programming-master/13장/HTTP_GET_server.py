# HTTP GET 요청을 처리하는 서버 프로그램

from http.server import BaseHTTPRequestHandler
from urllib import parse

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #URL 요청을 분석
        parsed_path = parse.urlparse(self.path)
        
        #응답 메시지의 기본 구성
        #self.xxx는 BaseHTTPRequestHandler의 속성이다
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address, #(host, port)
                self.address_string()), #클라이언트 주소 반환
            'command={}'.format(self.command), #요청 유형
            'path={}'.format(self.path), #요청 URL
            'real path={}'.format(parsed_path.path), #요청 URL의 path 정보
            'query={}'.format(parsed_path.query), #요청 URL의 query 정보
            'request_version={}'.format(self.request_version), #요청의 버전, HTTP/1.0
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version), #서버 소프트웨어 버전, BaseHTTP/0.2
            'sys_version={}'.format(self.sys_version), #파이썬 시스템 버전
            'protocol_version={}'.format(self.protocol_version), #HTTP 프로토콜 버전, HTTP/1.0
            '',
            'HEADERS RECEIVED:',
        ]
        
        #요청 헤더 정보를 응답 메시지에 추가
        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        
        #응답 헤더 전송
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        #응답 메시지 전송
        self.wfile.write(message.encode('utf-8'))

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
