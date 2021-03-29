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
