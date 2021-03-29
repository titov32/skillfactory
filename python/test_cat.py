from cat import Cat

sam = Cat('Сэм')
sam.set_age(2)
sam.set_gender('male')

baron = Cat('Барон')
baron.set_age(2)
baron.set_gender('male')

for i in sam, baron:
    print(f'Имя {i.name}')
    print(f'Возраст {i.get_age()}')
    print(f'Пол {i.get_gender()}')
    print(f'Вид животного {i.kind}')