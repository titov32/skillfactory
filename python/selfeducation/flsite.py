from flask import Flask, render_template, url_for, request
from parsing import ParserSS
from time import sleep
app = Flask(__name__)
title = 'offigne'
menu = [{'name': 'Установка', 'url': 'install-flask'},
        {'name': 'Первое использование', 'url': "first-app"},
        {"name": 'Обратная связь', 'url': 'contact'}]


@app.route('/test')
def index():
    return render_template('index.html', title='variable', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='about flask', menu=menu)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print(request.form)
    if request.method == 'GET':
        print('Work Method GET', request.form)
    return render_template('contact.html', title='Обратная связь', menu=menu)


@app.route('/parse', methods=['GET','POST'])
def parse():
    if request.method == 'POST':
        print(request.form)
    a = ParserSS()
    a.register()
    try:
        url_parsing = request.form.get('url_parsing')
        #'http://portal/guides/users/show?id=107592'
        #if 'guides' in url_parsing and 'users' in url_parsing:
        id_user = url_parsing.split('id=')[-1]
    except Exception as e:
        print('Ошибка ввода ', e)
        id_user = '97735'

    e = a.parse_employ(id_user)
    print('Фамилия', e['family'])
    print('special', e['special'])
    print('department', e['department'])
    print('tabel', e['tabel'])
    return render_template('permit.html', employ=e)


@app.route('/parse_unbound', methods=['GET','POST'])
def parse_unbound():
    if request.method == 'POST':
        print(request.form)
    a = ParserSS()
    a.register()
    list_id_unbound = a.parse_skud()
    employs = []
    for id_user in list_id_unbound:
        e = a.parse_employ(id_user)
        if e:
            employs.append(e)
        sleep(0.3)
        print(id_user)
    print(employs)
    return render_template('permits.html', employs=employs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
