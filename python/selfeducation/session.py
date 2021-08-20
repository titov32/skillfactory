from parsing import parse_employ, header

import requests
import pickle
profile_info = 'http://portal.stryservice.net/guides/users/show?id=107493'
session2 = requests.Session()
with open('cookies.pickle', 'rb') as f:
	cookies_dict = pickle.load(f)

employ = parse_employ(profile_info, headers=header, cookies_dict=cookies_dict)

print('Фамилия', employ['family'])
print('special', employ['special'])
print('tabel', employ['tabel'])
