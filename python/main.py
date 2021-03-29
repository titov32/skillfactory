from lib import check_win_positions, check_defend_posions, is_better_turn, side_selection

win_x = set()


coordinate = [[], [], []]


def init_conditions():
    """This function realize system coordinate and strategy set gamers"""

    for i in range(3):
        win_x.add(((i, 0), (i, 1), (i, 2)))
        win_x.add(((0, i), (1, i), (2, i)))

    win_x.add(((0, 0), (1, 1), (2, 2)))
    win_x.add(((0, 2), (1, 1), (2, 0)))


    for i in range(3):
        for j in range(3):
            coordinate[i].append('-')


def draw(coordinate):
    """This function draw grid coordinate"""
    print(' 0  1  2')
    for positions, value in enumerate(coordinate):
        print(positions, *value)


def difference_win(set_gamer, turn):
    """This function deleted lose strategy and return set which may be lead to success
    set_gamer: set
    turn: tuple - coordinate turn
    """
    temp_set = set()
    for item in set_gamer:
        if turn in item:
            temp_set.add(item)
    set_gamer -= temp_set
    return set_gamer


def show_win_strategy(set_):
    for i in set_:
        print(i)


def game_run(players):
    if 'x' == players['gamer']:
        next_turn=turn_gamer
    else:
        next_turn=turn_bot
    while True:
        if check_state(players):
            print('Game over')
            print(check_state(players))
            draw(coordinate)
            break
        else:
            next_turn()


def turn_round(side):
    """выбирает кто делает ход и запускает либо функцию хода игрока либо функцию хода бота"""
    pass

def check_state(players):
    """ПРоверка состояния игры """
    for pos in win_etalon:
        if len(pos & players['gamer_turn']==3):
            return 'gamer_win'
        if len(pos & players['bot_turn']==3):
            return 'bot_win'
        if players['gamer_win']==0==players['bot_win']:
            return 'standoff'
    return None

def turn_gamer(players, coordinate, player):
    global turn_bot
    while True:
        print('Введите координаты хода через пробел')
        turn = input()
        try:
            turn=turn.split()
            turn=int(turn[0]), int(turn[1])
            print(turn)
        except:
            print('Введены не корокетные значения')
            continue
        try:
            if coordinate[turn[0]][turn[1]]=='-':
                coordinate[turn[0]][turn[1]]=players[player]
                break
            else:
                print('Координата занята')
                continue
        except:
            print('Введите координаты из диапозона 0-2')
            continue
  #  difference_win(players['bot_win'],turn)
#    next_turn = turn_bot
    players['gamer_turn'].add(turn)
    # return turn, next_turn
    return turn

init_conditions()
win_0=win_x.copy()
win_etalon=win_x.copy()
players = side_selection()
print(f"gamer={players['gamer']}  bot={players['bot']}")
#turn_bot = turn_gamer(players, coordinate, 'bot')
if players['gamer']=='x':
    players['gamer_win']=win_x
    players['bot_win'] = win_0
else:
    players['gamer_win'] = win_0
    players['bot_win'] = win_x
players['gamer_turn']=set()
players['bot_turn']=set()


print('show win strategy for bot')
show_win_strategy(players['bot_win'])
draw(coordinate)
#game_run(players)
turn_gamer(players, coordinate, 'gamer')

print('___________')
print('show win strategy for bot')
show_win_strategy(players['bot_win'])
print('show win strategy for player')
show_win_strategy(players['gamer_win'])





