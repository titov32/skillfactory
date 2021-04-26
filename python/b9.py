import json

import requests

r = requests.get('https://baconipsum.com/api/?type=meat-and-filler') # отправляем пост запрос
text=json.loads(r.content)
print(text[0])

import requests  # импортируем наш знакомый модуль
import lxml.html
from lxml import etree

html = requests.get('https://www.python.org/').content  # получим html главной странички официального сайта python

tree = lxml.html.document_fromstring(html)
# забираем текст тега <title> из тега <head> который лежит в свою очередь внутри тега <html> (в этом невидимом теге <head> у нас хранится основная информация о страничке. Её название и инструкции по отображению в браузере.

ul = tree.findall('/html/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li[1]/time')
# создаём цикл в котором мы будем выводить название каждого элемента из списка
for li in ul:
    a = li.find('a') # в каждом элементе находим где хранится заголовок новости. У нас это тег <a>. Т.е. гиперссылка на которую нужно нажать, чтобы перейти на страницу с новостью. (Гиперссылки в html это всегда тэг <a>)
    print(a.text) # из этого тега забираем текст - это и будет нашим названием

print(title)  # выводим полученный заголовок страницы
tree2 = etree.parse('b9.html', lxml.html.HTMLParser())
tag2=tree2.xpath('/html/body/tag1/tag2/text()')
print('________________')
print(tag2)

#ul = tree.findall('body/div/div[3]/div/section/div[3]/div[1]/div/ul/li')