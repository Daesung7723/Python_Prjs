from urllib import parse

url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"
p_url = parse.urlparse(url)

print('schme: ',p_url.scheme)
print('netloc: ',p_url.netloc)
print('path: ',p_url.path)
print('params: ',p_url.params)
print('query: ',p_url.query)
print('fragment: ',p_url.fragment)

tuple_url = parse.urlsplit("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")
print('\nSplitted URL: ', tuple_url)
