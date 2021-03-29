"""
def turn_bot():
    turn = check_win_positions(players['bot_win'] )
    if turn:
        return turn
        players['bot_turn'].add(turn)
    check_defend_posions()
    if is_better_turn[0]:
        return is_better_turn[1]
    else:
        return another_turn
"""



def check_win_positions(win_positions):
    """делает обход всех выйгрышных позиций и если есть строчка с двумя элементами то возвращает третий"""
    for item in win_positions:
        if (turn_bot.diffence(item)) == 2:
            return (item - turn_bot)


def check_defend_posions():
    """делает обход всех пройгрышных позиций и если есть строчка с двумя элементами то возвращает третий"""


def is_better_turn():
    """проверяет есть ли ход после которого не придется защищаться"""
    """
    0 проверяем 
    """


def side_selection():
    players = {}
    while True:
        print('Выберите сторону 0 или x')
        gamer = input()
        if gamer == '0' or gamer == 'x':
            if gamer == '0':
                players['bot'] = 'x'
                players['gamer'] = '0'
                return players
            else:
                players['bot'] = '0'
                players['gamer'] = 'x'
                return players
        else:
            print('Введите корректные данные')
            continue



class Gamer():
    def __init__(self, side):
        self.side=side
        self.turns = ()

    def turn_pass (self, coordinate):
        while True:
            print('Введите координаты хода через пробел')
            turn = input()
            try:
                turn = turn.split()
                turn = int(turn[0]), int(turn[1])
                print(turn)
            except:
                print('Введены не корокетные значения')
                continue
            try:
                if coordinate[turn[0]][turn[1]] == '-':
                    coordinate[turn[0]][turn[1]] = players[player]
                    break
                else:
                    print('Координата занята')
                    continue
            except:
                print('Введите координаты из диапозона 0-2')
                continue