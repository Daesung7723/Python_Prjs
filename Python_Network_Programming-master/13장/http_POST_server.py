# HTTP POST request를 처리하는 서버 프로그램

import cgi
from http.server import BaseHTTPRequestHandler
import io


class PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # POST 데이터 분석
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # 응답 전송
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        out.write('Client: {}\n'.format(self.client_address))
        out.write('User-agent: {}\n'.format(
            self.headers['user-agent']))
        out.write('Path: {}\n'.format(self.path))
        out.write('Form data:\n')

        # POST 정보를 다시 전송
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # field가 업로드 파일 포함
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                out.write(
                    '\tUploaded {} as {!r} ({} bytes)\n'.format(
                        field, field_item.filename, file_len)
                )
            else:
                # 레귤라 폼으로 전송
                out.write('\t{}={}\n'.format(
                    field, form[field].value))

        # 연결 분리
        out.detach()


if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
