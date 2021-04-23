from requests import get
import json
from redis import Redis
from time import time
from config import *

redis_conn = Redis(host, port)
VAL=[]
for val in exchanges:
    VAL.append(exchanges[val])

VAL.remove('EUR')

params = {
    'access_key': access_key,
}
class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def set_val():
        print('Обновляем кэш')
        rate = {}
        for val in VAL:
            r = get(f'http://api.exchangeratesapi.io/latest?symbols={val}', params=params)
            a = json.loads(r.content)
            rate[val] = a['rates'][val]
            redis_conn.set(val, rate[val])
            redis_conn.set('time', time())
        return rate

    @staticmethod
    def get_val():
        rate = {}
        print('Берем данные из кэша')
        for val in VAL:
            rate[val] = float(redis_conn.get(val).decode('utf8'))
        return rate

    @staticmethod
    def check_val(raw_in_val:str, raw_out_val:str):
        try:
            in_val = exchanges[raw_in_val.lower()]
        except KeyError:
            raise APIException(f'Валюты {raw_in_val.lower()} не найдено')
        try:
            out_val = exchanges[raw_out_val]
        except KeyError:
            raise APIException(f'Валюты {raw_out_val} не найдено')
        if in_val==out_val:
            raise APIException('Попробуй разные валюты')
        return in_val, out_val

    @staticmethod
    def get_price(raw_in_val: str, raw_out_val: str, sum=1):
        #проверяем корректность на ошибки
        in_val, out_val = Converter.check_val(raw_in_val, raw_out_val)
        # проверяем свежесть данных если старше 20 минут то запршиваем заново, если нет берем из кэша
        if not redis_conn.get('time'):
            rate = Converter.set_val()
        elif time() - float(redis_conn.get('time').decode('utf8')) > 1200:
            rate = Converter.set_val()
        else:
            rate = Converter.get_val()
        # Обрабатываем данные полученные из ввода
        if in_val == 'EUR':
            return rate[out_val] * sum

        if out_val == 'EUR':
            return 1 / rate[in_val] * sum

        if in_val == 'RUB' and out_val == 'USD' or \
                in_val == 'USD' and out_val == 'RUB':
            return rate[out_val] / rate[in_val] * sum


# test Converter
a = Converter()
print('Цена 1000 Евро в рублях')
print(a.get_price('ЕВРО', 'рубль', 1000))

print('Цена 1000 долларов в рублях')
print(a.get_price('доллар', 'рубль', 1000))
