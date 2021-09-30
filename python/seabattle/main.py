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

    def __hash__(self):
        return hash((self.x, self.y))


class Ship:
    def __init__(self, stern, size, position_vertical):
        self.stern = stern
        self.size = size
        self.position_vertical = position_vertical
        self.contur = []
        self.ship_position = []
        self.draw_contur()
        self.start_condition()

    def __str__(self):
        return f'{self.ship_position}'

    def __contains__(self, dot):
        if dot in self.ship_position:
            if dot.condition == '■':
                return True
        else:
            return False

    def draw_contur(self):
        x, y = self.stern.x, self.stern.y
        if self.position_vertical:
            self.ship_position = [Dot(x, i) for i in range(y, y + self.size)]
            for i in range(y - 1, y + self.size + 1):
                self.contur.extend([Dot(x - 1, i), Dot(x, i), Dot(x + 1, i)])
        else:
            self.ship_position = [Dot(i, y) for i in range(x, x + self.size)]
            for i in range(x - 1, x + self.size + 1):
                self.contur.extend([Dot(i, y - 1), Dot(i, y), Dot(i, y + 1)])

    def start_condition(self):
        for i in self.ship_position:
            i.condition = '■'

    def is_dead(self):
        count = 0
        for dot in self.ship_position:
            if dot.condition == '■':
                count += 1
        if count == 0:
            return True
        else:
            return False

    def shot(self, dot):
        if dot not in self.ship_position:
            return 'mimo'
        else:
            position = self.ship_position.index(dot)
            self.ship_position[position].condition = 'X'
            print(('Попал'))
        if self.is_dead():
            print('The ship is dead')


class Board:
    def __init__(self, size):
        self.size = size
        self.fields = [[Dot(x, y) for x in range(size)] for y in range(size)]
        self.placing_fields = []
        self.border = []
        self.ships = []
        self.fill_border()
        self.place_ships()

    def __contains__(self, item):
        for coord in self.fields:
            if item in coord:
                return True
        return False

    def place_ships(self):
        ships_size = [3, 2, 2, 1, 1, 1, 1]
        for size in ships_size:
            while True:
                ship = Ship(Dot(randint(0, size_board), randint(0, size_board)), size, randint(0, 1))
                if self.append_good(ship):
                    self.ships.append(ship)
                    break

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
        set_ship_contur = set(ship.contur)

        set_ship_position = set(ship.ship_position)

        set_placing_fields = set(self.placing_fields)

        set_border = set(self.border)
        if set_ship_contur.intersection(set_placing_fields) or set_ship_position.intersection(set_border):
            return False
        else:
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
            return False

    def show_board(self):
        tmp_list = [str(i) for i in range(self.size - 1)]
        os_x = '  ' + ' '.join(tmp_list)
        print(os_x)
        for count, i in enumerate(board.fields[:-1]):
            print(count, end=' ')
            for j in i[:-1]:
                print(j, end=' ')
            print()


class Player:
    def __init__(self):
        self.board = Board(size_board)

    def shot(self, dot):
        pass


class Bot:
    pass


class App:
    def __init__(self):
        # self.player1 = Player
        # self.player2 = Player
        self.board_human = Board(7)
        self.board_bot = Board(7)

    def initial(self):
        print('Приветствуем Вас в игре морской бой')
        print('Для стрельбы введите координты через пробел')

    def run(self):
        while True:

            try:
                x, y = input('введите кординаты через пробел   ').split(' ')
                x = int(x)
                y = int(y)

            except ValueError:
                print('введите 2 корректныx значения')
                continue


if __name__ == '__main__':
    size_board = 7
    board = Board(size_board + 1)

    board.show_board()

    a = Dot(1, 1)
    ship1 = Ship(a, 3, 1)
    b = Dot(5, 1)
    ship2 = Ship(b, 2, 1)
    l = [ship1, ship2]

    game = App()
    game.initial()
    #game.run()
