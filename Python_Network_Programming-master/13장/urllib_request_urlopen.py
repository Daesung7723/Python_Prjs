# GET request 보내기와 서버 응답 출력 프로그램

from urllib import request

URL = 'https://www.dongyang.ac.kr/' #url
response = request.urlopen(URL) #GET request와 서버 응답
print('RESPONSE:', response)
print('URL :', response.url) #url 정보

headers = response.headers #응답 헤더 정보
print('DATE :', headers['date'])
print('HEADERS :')
print('---------')
print(headers)

data = response.read().decode('utf-8') #응답 내용 읽기
print('LENGTH :', len(data))
print('DATA :')
print('---------')
print(data)
