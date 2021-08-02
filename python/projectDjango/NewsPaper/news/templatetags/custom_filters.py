from django import template
CENSOR = {'пизда', 'хуй', 'блядь', 'пиздец', 'залупа', 'пизде', 'пизду', 'хуюшка', 'нахуй'}
register = template.Library()

@register.filter(name='multiply') # регестрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg): # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргуменит — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    return str(value) * arg # возвращаемое функцией значение — это то значение, которой подставится к нам в шаблон


@register.filter(name='censor') # регестрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def censor(raw): # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргуменит — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    list_word = raw.split()
    clear_text = ''
    word=''
    for i in list_word:
        if '.' or ',' in i:
            word = i.replace(',', '')
            word = i.replace('.', '')
        if not word.lower() in CENSOR:
            clear_text += i + ' '
        else:
            clear_text += 'censor '
    return clear_text