"""
Для работы нужно создать файл setting.py cо следующим содержимым
USER = {
            'login': 'имя_пользователя_при_входе_в_портал',
            'domain': 'имя_домена',
            'password': 'ваш_пароль'
        }
"""

import requests
from bs4 import BeautifulSoup
import pickle
from setting import USER, CONN_REDIS

ORGANISATIONS = {
    'Стройсервис': (16, 1),
    'Губахинский кокс': (22, 2),
    'Шахта № 12': (18, 3),
    'Белтранс': (14, 4),
    'Барзасское товарищество': (32, 5),
    'Пермяковский': (25, 6),
    'Березовский': (25, 8),
    'Беловопромжелдортранс': (27, 9),
    'Шестаки': (19, 10),
    'Аврора': (12, 12),
    'Зиминский': (22, 13),
    'Федерация тайского бокса России': (37, 15),
}


def job(text_organisation):
    for org in ORGANISATIONS:
        if org in text_organisation:
            name_org = text_organisation[:ORGANISATIONS[org][0]]
            special = text_organisation[ORGANISATIONS[org][0]:]
            return name_org, special
class ParserSS:
    def __init__(self):
        self.session = requests.Session()
        self.url = 'http://portal.stryservice.net'
        self.auth_url = 'http://portal.stryservice.net/auth'
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        self.cookies_dict = []
        self.data = USER
        self.connection = CONN_REDIS
    def auth(self):
        try:
            self.session = requests.Session()
            self.response = self.session.post(self.auth_url, data=self.data, headers=self.header)
            self.cookies_dict = [
                {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
                for key in self.session.cookies
            ]
        except Exception as e:
            print(f'ошибка аунтификации {e}')
        print('Запись куки в файл')
        with open('cookies', 'wb') as file:
            pickle.dump(self.cookies_dict, file)
        print('Запись куки в файл завершена')

    def register(self):
        try:
            print('Чтение куки из файла')
            if not self.session.cookies.items():
                with open('cookies', 'rb') as f:
                    self.cookies_dict = pickle.load(f)
                    print('чтение из куки завершена')
            for cookies in self.cookies_dict:
                self.session.cookies.set(**cookies)
                print('запись куки в сессию завершена')
        except FileNotFoundError:
            self.auth()
        except Exception as e:
            print(f'Проблемы! Ошибка регистрации {e}')

    def parse_employ(self, id_user):
        context_permit = {'id':id_user}
        profile_info = 'http://portal.stryservice.net/guides/users/show?id='+id_user
        profile_response = self.session.get(profile_info, headers=self.header).text

        soup_employ = BeautifulSoup(profile_response, 'html.parser')
        block1 = soup_employ.find_all("div",
                                      class_="d-flex flex-column align-items-center justify-content-center p-4 "
                                             "show-child-on-hover hide-child-on-hover")[0]

        employ = block1.find('h5', class_='mb-0 fw-700 text-center mt-3')

        special = employ.find_all(class_='text-muted mb-0')[0].text
        context_permit['special'] = special
        department = employ.find_all(class_='text-muted mb-0 hide-on-hover-parent')[0].text
        #context_permit['department'] = department
        #context_permit['organisation'] = department[:18]
        context_permit['organisation'], context_permit['department'] = job(department)
        context_permit['job'] = department

        fio1 = employ.text

        fio2 = fio1.split(special)[0]
        a = fio2.split(' ')

        list2 = [i for i in a if i != '\n' and i != '']
        context_permit['family'] = list2[0]
        context_permit['name'] = list2[1]
        context_permit['patronymic'] = list2[2][:-1]

        block2 = soup_employ.find_all("div",
                                      class_="card-body py-0 px-4 border-faded border-right-0 border-bottom-0 "
                                             "border-left-0 pt-4")[0]
        tabel_number = block2.find('dd', class_='col-sm-9').text
        context_permit['tabel'] = tabel_number
        try:
            block_image = block1.find('a', class_='js-highslide').get('href')
            image_bytes = requests.get(f'{self.url}{block_image}').content
            with open(f'static/img/{id_user}.jpg', 'wb') as file:
                file.write(image_bytes)
        except AttributeError:
            print('Foto no exist')
            block_image=None
            return None

        context_permit['foto'] = f'{id_user}.jpg'

        return context_permit

    def parse_skud(self):
        list_id_employ = []
        link = self.url + '/guides/tools/skud?q=&company=3&type=unbound_skud'
        skud_response = self.session.get(link, headers=self.header).text
        soup_employ = BeautifulSoup(skud_response, 'lxml')
        div_table = soup_employ.find_all('div', class_='card-body container-fluid')[0]
        block1 = div_table.find_all("table", class_="table table-sm table-hover mt-3")[0]
        employs = block1.find_all('a')
        for e in employs:
            id_user = e.get('href').split('id=')[-1]
            list_id_employ.append(id_user)
        return list_id_employ

    def check_redis(self, id_user):
        data={}
        if self.connection.hgetall(id_user):
            raw_data = self.connection.hgetall(id_user)
            data['id_user'] = id_user
            data['tabel'] = raw_data[b'tabel'].decode('utf8')
            data['family'] = raw_data[b'family'].decode('utf8')
            data['name'] = raw_data[b'name'].decode('utf8')
            data['patronymic'] = raw_data[b'patronymic'].decode('utf8')
            data['department'] = raw_data[b'department'].decode('utf8')
            data['organisation'] = raw_data[b'organisation'].decode('utf8')
            data['special'] = raw_data[b'special'].decode('utf8')
            return data
        else:
            data = self.parse_employ(id_user)
            self.connection.hmset(id_user, data)
            return data


if __name__ == "__main__":

    a = ParserSS()
    a.register()

    employ = a.check_redis('86292')
    print('Фамилия', employ['family'])
    print('special', employ['special'])
    print('department', employ['department'])
    print('organisation', employ['organisation'])
    print('tabel', employ['tabel'])

"""     list_id = a.parse_skud()
    for i in list_id:
        employ = a.parse_employ(i)
        if employ:
            print('Фамилия', employ['family'])
            print('special', employ['special'])
            print('tabel', employ['tabel'])
            print('department', employ['department'])
"""
# https://www.youtube.com/watch?v=IEfQLbxHY_g&list=PL6plRXMq5RACy7NhEK4tdLeKxmKmxDIrr&index=8&ab_channel=ZProger%5BIT%5D
