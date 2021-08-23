import requests
import fake_useragent
from bs4 import BeautifulSoup

#session
# Authorization
#Get/Set cookies
# для сохранения данных сессии  и кукис лучше использовать сессии
session = requests.Session()

# ссылка для ввода логина пароля, можно посмотреть через сеть в браузере
link = 'http://portal.stryservice.net/auth'

user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'

header = {
	'user-agent': user
}

# поля запроса можно посмотреть что передает браузер в запросе
data = {
	'login': 'e.titov',
	'domain': 'SHAHTA12',
	'password' : '47tit_evg'
}

responce = session.post(link, data=data, headers=header)

# ссылка для проверки авторизации
profile_info = 'http://portal.stryservice.net/profile'
profile_responce = session.get(profile_info, headers=header).text
print(profile_responce)

cookies_dict = [
	{"domain": key.domain, "name": key.name, "path" : key.path, "value": key.value}
	for key in session.cookies
]

#session2 = requests.Session()

#for cookies in cookies_dict:
#	session2.cookies.set(**cookies)

#resp = session2.get(profile_info, headers=header)
#print(resp.text)