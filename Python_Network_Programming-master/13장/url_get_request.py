# GET request 발송 프로그램

from urllib import parse
from urllib import request

query = {'name': 'YKSUH', 'position': 'professor'} #query를 딕셔너리로 표현
encoded_query = parse.urlencode(query) #딕셔너리에서 query URL 생성
print('Encoded:', encoded_query)

url = 'http://localhost:8080/?' + encoded_query
#url = 'https://httpbin.org/get'
resp = request.urlopen(url)
print(resp.read().decode('utf-8'))
