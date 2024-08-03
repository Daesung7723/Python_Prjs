#간단한 Web 서버

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #GET 요청에 대한 응답 전송
        self.send_response(200) #헤더 송신
        self.end_headers()
        
        self.wfile.write(b'Hello, world!') #응답 메시지

    def do_POST(self):       
        #응답 헤더 전송
        self.send_response(200) 
        self.end_headers()
        
        #응답 메시지 전송
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length) #요청 내용을 읽어온다
        response = BytesIO()#응답을 바이트 스트림에 저장
        response.write(b'POST request: ')
        response.write(b'Response: ')
        response.write(body) #요청 내용을 응답에 추가
        self.wfile.write(response.getvalue()) #응답 전송

#서버 객체 생성
httpd = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever() #서버 실행
