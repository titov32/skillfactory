import requests
from bs4 import BeautifulSoup
import pickle

# session
# Authorization
# Get/Set cookies
# для сохранения данных сессии  и кукис лучше использовать сессии
user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
header = {
    'user-agent': user
}

def auth_ss(header):
    session = requests.Session()
    proxy = '192.168.24.254'
    # ссылка для ввода логина пароля, можно посмотреть через сеть в браузере
    link = 'http://portal.stryservice.net/auth'

    # поля запроса можно посмотреть что передает браузер в запросе
    data = {
        'login': 'e.titov',
        'domain': 'SHAHTA12',
        'password': '47tit_evg'
    }

    response = session.post(link, data=data, headers=header)

    cookies_dict = [
        {"domain": key.domain,
         "name": key.name,
         "path": key.path,
         "value": key.value}
        for key in session.cookies
    ]
    with open('cookies', 'wb') as file:
        pickle.dump(cookies_dict, file)

    return response, cookies_dict

def parse_employ(profile_info, cookies_dict={}, headers=header):
    context_permit = {}
    session = requests.Session()
    if cookies_dict:
        for cookies in cookies_dict:
            session.cookies.set(**cookies)

    profile_response = session.get(profile_info, headers).text

    soup_employ = BeautifulSoup(profile_response, 'lxml')
    block1 = soup_employ.find_all("div",
                                  class_="d-flex flex-column align-items-center justify-content-center p-4 show-child-on-hover hide-child-on-hover")[
        0]

    employ = block1.find('h5', class_='mb-0 fw-700 text-center mt-3')

    special = employ.find_all(class_='text-muted mb-0')[0].text
    context_permit['special'] = special
    department = employ.find_all(class_='text-muted mb-0 hide-on-hover-parent')[0].text
    context_permit['department'] = department

    fio1 = employ.text

    fio2 = fio1.split(special)[0]
    a = fio2.split(' ')

    list2 = [i for i in a if i != '\n' and i != '']
    context_permit['family'] = list2[0]
    context_permit['name'] = list2[1]
    context_permit['patronymic'] = list2[2][:-1]

    block2 = soup_employ.find_all("div",
                                  class_="card-body py-0 px-4 border-faded border-right-0 border-bottom-0 border-left-0 pt-4")[
        0]
    tabel_number = block2.find('dd', class_='col-sm-9').text
    context_permit['tabel'] = tabel_number


    return context_permit





if __name__ == "__main__":
    try:
        with open('cookies', 'rb') as f:
            cookies_dict = pickle.load(f)
    except Exception as e:
        print(f'Ошибка чтения файла {e}')
        response, cookies_dict = auth_ss(header)

    employ = parse_employ(profile_info='http://portal.stryservice.net/guides/users/show?id=104489',
                          cookies_dict=cookies_dict,
                          headers=header)
    print('Фамилия', employ['family'])
    print('special', employ['special'])
    print('tabel', employ['tabel'])

# https://www.youtube.com/watch?v=IEfQLbxHY_g&list=PL6plRXMq5RACy7NhEK4tdLeKxmKmxDIrr&index=8&ab_channel=ZProger%5BIT%5D
