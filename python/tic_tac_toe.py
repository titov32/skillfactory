class Player:
    def __init__(self, state):
        self.state = state
        self.turns = []

    def __str__(self):
        return '%s' % self.state

    def __repr__(self):
        return '%s' % self.state

    def turn(self):
        while True:
            print('Введите кооры через пробел')
            try:
                spisok = input().split()
                x, y = int(spisok[0]), int(spisok[1])
            except ValueError:
                print('Введите корректные значения')
                continue
            # добавить проверки на занятость полей
            if 0<=x<=2 and 0<=y<=2:
                self.turns.append((x, y))
            else:
                print('Введите коордиинаты от 0 до 2')
                continue
            return x, y

    def get_turn(self):
        return self.turns


class GameRound:
    def __init__(self, player1, player2):
        self.grid = [[], [], []]
        for i in range(3):
            for j in range(3):
                self.grid[i].append('-')
        self.win = set()
        for i in range(3):
            self.win.add(((i, 0), (i, 1), (i, 2)))
            self.win.add(((0, i), (1, i), (2, i)))

        self.win.add(((0, 0), (1, 1), (2, 2)))
        self.win.add(((0, 2), (1, 1), (2, 0)))
        self.players = [Player(player1), Player(player2)]
        self.round = 1

    def draw(self):
        print('    0    1    2')
        for val, pos in enumerate(self.grid):
            print(val, pos)

    def check_win_positions(self, turns):
        for i in self.win:
            if len(set(i).intersection(set(turns))) == 3:
                return True
        return False


    def next_turn(self):
        self.draw()
        while self.round <= 9:
            print('Сейчас ходит', self.players[0])

            while True:
                i, j = self.players[0].turn()
                if self.grid[i][j] =='-':
                    self.grid[i][j]=self.players[0].state
                    break
                else:
                    print('Поле занято')
            if self.check_win_positions(self.players[0].get_turn()):
                print(self.players[0].state, '  Победил')
                self.draw()
                return self.players[0].state
            self.players.append(self.players.pop(0))  # меняем очередность игроков
            self.round += 1
            self.draw()
        print('Ничья')
        return 'Ничья'



vasy = Player('x')
pety = Player('0')
print('state', vasy.state)
game = GameRound(vasy, pety)
game.next_turn()
