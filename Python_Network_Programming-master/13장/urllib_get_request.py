# GET request 발송 프로그램

from urllib import parse
from urllib import request

query = {'name': 'YKSUH', 'position':'professor'} #query를 딕셔너리로 표현
encoded_query = parse.urlencode(query) #딕셔너리로부터 query URL 생성
print('Encoded:', encoded_query)

url = 'http://localhost:8080/?' + encoded_query #HTTP_GET_server.py 필요
#url = 'https://httpbin.org/get'
resp = request.urlopen(url) #GET request와 응답
print(resp.read().decode('utf-8'))
