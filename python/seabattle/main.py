from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.condition = 'O'

    def __repr__(self):
        return f'Dot({self.x},{self.y})'

    def __str__(self):
        return self.condition

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class Ship:
    def __init__(self, stern, size, position_vertical):
        self.stern = stern
        self.size = size
        self.position_vertical = position_vertical
        self.contur = []
        self.ship_position = []
        self.draw_contur()

    def __str__(self):
        return f'{self.ship_position}'

    def draw_contur(self):
        x, y = self.stern.x, self.stern.y
        if self.position_vertical:
            self.contur.extend([Dot(x, y - 1), Dot(x-1, y-1), Dot(x+1, y-1)])
            for i in range(y, y + self.size):
                self.contur.extend([Dot(x - 1, i), Dot(x + 1, i), Dot(x + 1, i)])

                self.ship_position.append(Dot(x, i))

            self.contur.extend([Dot(x, y + self.size), Dot(x-1, y + self.size), Dot(x+1, y + self.size)])
        else:
            self.contur.extend([Dot(x - 1, y), Dot(x - 1, y-1), Dot(x - 1, y+1)])
            for i in range(x, x + self.size):
                self.contur.append(Dot(i, y - 1))
                self.contur.append(Dot(i, y))
                self.ship_position.append(Dot(i, y))
                self.contur.append(Dot(i, y + 1))
            self.contur.append(Dot(x + self.size, y))


class Board:
    def __init__(self, size):
        self.fields = [[Dot(x, y) for x in range(size)] for y in range(size)]
        self.placing_fields=[]
        self.border = []
        self.fill_border()

    def __contains__(self, item):
        for coord in self.fields:
            if item in coord:
                return True
        return False

    def fill_border(self):
        """"
        метод определяет границы справа и снизу
        """
        self.border = [i[-1] for i in self.fields]
        self.border.extend(self.fields[-1])

    def is_placing(self, ship):
        """
        проверяет размещение корабля на доске
        :param ship: Ship
        :return: bool
        """
        for coord in ship.contur:
            if coord in self.placing_fields:
                return False
        for coord in ship.ship_position:
            if coord in self.border:
                return False
        return True

    def append_good(self, ship):
        try:
            if self.is_placing(ship):
                for coord in ship.ship_position:
                    self.fields[coord.x][coord.y].condition = '■'
                    self.placing_fields.extend(ship.ship_position)
                return True
            else:
                return False
        except IndexError:
            print('Добавление не возможно')
            return False

if __name__ == '__main__':
    size_board = 7
    board = Board(size_board+1)
    ships_size = [3, 2, 2, 1, 1, 1, 1]
    for size in ships_size:
        while True:
            ship = Ship(Dot(randint(0,size_board), randint(0,size_board)), size, randint(0,1))
            if board.append_good(ship):
                print(f'корабль {ship} добавлен')
                break
            else:
                print(f'корабль {ship} не добавлен')



    print('0 1 2 3 4 5 6')
    for i in board.fields[:-1]:
        for j in i[:-1]:
            print(j, end=' ')
        print()
