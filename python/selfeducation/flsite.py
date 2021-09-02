from flask import Flask, render_template, url_for, request
from parsing import ParserSS
from time import sleep

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/parse', methods=['GET', 'POST'])
def parse():
    a = ParserSS()
    a.register()
    if request.method == 'POST':
        print(request.form)

        url_parsing = request.form.get('url_parsing')
        print(url_parsing, ' это переменная url parsing')

        if not url_parsing:
            print('ветка1')
            return render_template('permit_not_found.html')
        try:
            print('ветка2')
            id_user = url_parsing.split('id=')[-1]
        except Exception as e:
            print('Ошибка ввода ', e)

        e = a.parse_employ(id_user)
        print('Фамилия', e['family'])
        print('special', e['special'])
        print('department', e['department'])
        print('tabel', e['tabel'])
        return render_template('permit.html', employ=e)
    else:
        r = a.parse_employ('9')
        return render_template('permit.html', employ=r)

@app.route('/parse_unbound', methods=['GET', 'POST'])
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


@app.route('/parse_unbound_one_permit', methods=['GET', 'POST'])
def parse_unbound_one_permit():
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
    return render_template('print_one_permit.html', employs=employs)


@app.route('/parse/<id>/')
def parse_id(id):
    a = ParserSS()
    a.register()
    e = a.parse_employ(id)
    return render_template('permit_one.html', employ=e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
