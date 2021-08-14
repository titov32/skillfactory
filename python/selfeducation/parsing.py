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

user = fake_useragent.UserAgent().random

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
	for ke in session.cookies
]

session2 = requests.Session()

for cookies in cookies_dict:
	session2.cookies.set(**cookies)

resp = session2.get(profile_info, headers=header)
print(resp.text)





#https://www.youtube.com/watch?v=IEfQLbxHY_g&list=PL6plRXMq5RACy7NhEK4tdLeKxmKmxDIrr&index=8&ab_channel=ZProger%5BIT%5D