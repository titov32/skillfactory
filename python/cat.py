class Pet:
    def __init__(self, name, age=0, gender=None):
        self.name = name
        self.age = age
        self.gender = gender

    def set_age(self, age):
        if age >= 0 and isinstance(age, int):
            self.age = age

    def get_age(self):
        return self.age

    def set_gender(self, gender):
        if gender == 'male' or gender == 'female':
            self.gender = gender

    def get_gender(self):
        return self.gender


class Cat(Pet):
    def __init__(self, name, kind='Cat'):
        super().__init__(name)
        self.kind = 'Cat'


class Client:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def get_balance(self):
        print(f'{self.name} Баланс {self.balance}')
        return self.balance

    def pay(self, sum):
        if sum is float or sum is int:
            self.balance += sum


class Guests(Client):
    def __init__(self, name, balance=0):
        super().__init__(name, balance=0)
        self.status = ''
        self.city = ''

    def set_status(self, status):
        if isinstance(status, str):
            self.status = status

    def set_city(self, city):
        if isinstance(city, str):
            self.city = city

    def info(self):
        print(f'{self.name}, {self.city}, статус {self.status}')
