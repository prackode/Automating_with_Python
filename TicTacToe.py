from math import inf
import time
import random

'''
Created By Prakhar Agarwal
:)
'''


HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score 
        else:
            if score[2] < best[2]:
                best = score

    return best

def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    print(f'Computer turn [{c_choice}]')

    if depth == 9:
        x=random.choice([0,1,2])
        y=random.choice([0,1,2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)
    render(board, c_choice, h_choice)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    moves={
        1:[0,0],2:[0,1],3:[0,2],
        4:[1,0],5:[1,1],6:[1,2],
        7:[2,0],8:[2,1],9:[2,2],
        }
    move = int(input('Use numpad (1..9): '))
    coord = moves[move]
    can_move = set_move(coord[0], coord[1], HUMAN)
    render(board, c_choice, h_choice)

h_choice = input("What would you like to choose: O or X ").capitalize()
c_choice = ''
first = input('What you like to move first[y/n]: ').capitalize()
print("Let's Begin......")
time.sleep(1)
if h_choice == 'X':
    c_choice = 'O'

else:
    c_choice = 'X'

while len(empty_cells(board)) > 0 and not game_over(board):
    if first == 'N':
        ai_turn(c_choice, h_choice)
        first = ''
    
    human_turn(c_choice, h_choice)
    ai_turn(c_choice, h_choice)

time.sleep(1)
if wins(board, HUMAN):
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)
    print('HURRAY, YOU WIN!')

elif wins(board, COMP):
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)
    print('UH OH!! YOU LOSE!')

else:
    render(board, c_choice, h_choice)
    print('IT\'S A DRAW!')
