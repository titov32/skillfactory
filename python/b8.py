class ParentException(Exception):
    def __init__(self, messages,
                 error):  # допишем к нашему пустому классу конструктор, который будет печатать дополнительно в консоль информацию об ошибке.
        super().__init__(messages)  # помним про вызов конструктора родительского класса
        print(f"Errors: {error}")  # печатаем ошибку


class ChildException(ParentException):  # создаём пустой класс – исключение наследника, наследуемся от ParentException
    def __init__(self, messagef, error):
        super().__init__(messagef, error)


try:
    raise ChildException("messageff", "errorsss")  # поднимаем исключение-наследник, передаём дополнительный аргумент
except ParentException as e:
    print(e)  # выводим информацию об исключении

class NonPositiveDigitException(ZeroDivisionError):
    pass

class Square:
    def __init__(self, a):
        self.a=a

    def get_square(self):
        if self.a>0:
            return self.a**2
        else:
            raise NonPositiveDigitException('Сторона квадрата меньше 0')

a=Square(2)
b=Square(-2)
print(a.get_square())
print(b.get_square())