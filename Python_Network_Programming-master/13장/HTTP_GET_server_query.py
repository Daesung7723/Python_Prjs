#HTTP GET 서버 프로그램

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    #GET request를 처리한다
    def do_GET(self):
        parsed_path = parse.urlparse(self.path) #URL 분석
        msg = parsed_path.query #URL에서query를 찾는다
        if msg == '':
            return
        
        #query를 딕셔너리로 분해한다
        parsed_query = parse.parse_qs(msg)

        resp = "Fault" #허용되지 않은 query를 받았을 때 전송 메시지
        
        #query를 분석하여 응답 메시지를 구성한다
        try:
                if parsed_query["led"][0] == "on":
                        resp="The LED is ON"
                        
                elif parsed_query["led"][0] == "off":
                        resp="The LED is OFF"
                        
        except:
                pass

        #헤더 전송
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        
        #응답 전송
        self.wfile.write(resp.encode())

httpd = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
