# POST request 발송 프로그램

from urllib import parse
from urllib import request

data = {'tempeature': '25C', 'humidity': '60%'} #POST 데이터
encoded_data = parse.urlencode(data).encode('utf-8')
url = 'https://httpbin.org/post'
#url = 'http://localhost:8080/' #서버 지정
resp = request.urlopen(url, data=encoded_data) #POST request
print(resp.read().decode('utf-8'))
