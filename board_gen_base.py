import random
from colorama import Fore, Style

board_width = 10
board_height = 10
num_bombs = 20
b = 9

key = {"value": 0, "visibility": 0}

board = [[[attribute for attribute in key.values()] for _ in range(board_width)] for _ in range(board_height)]

def print_board_raw(board):
    for row in board:
        thingies = [value for value, _ in row]
        print(thingies)

def print_board(board, color=True):
    if color: colorize(board)
    for row in board:
        for col in row:
            print(col[0], end=' ')
        print()

# print_board_raw(board)

bomb_positions = random.sample(range(board_height*board_width), num_bombs)

# super cool :3
for pos in bomb_positions:
    board[pos // board_width][pos % board_width][0] = b

colors = {
    9: {'filler': 'X', 'color': Fore.RED},
    1: {'filler': '1', 'color': Fore.LIGHTBLUE_EX},
    2: {'filler': '2', 'color': Fore.GREEN},
    3: {'filler': '3', 'color': Fore.YELLOW},
    4: {'filler': '4', 'color': Fore.BLUE},
    5: {'filler': '5', 'color': Fore.RED},
    6: {'filler': '6', 'color': Fore.CYAN},
    7: {'filler': '7', 'color': Fore.MAGENTA},
    8: {'filler': '8', 'color': Fore.YELLOW},
    0: {'filler': '-', 'color': Fore.YELLOW},
}

def colorize(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            board[row][col][0] = f"{colors[board[row][col][0]]['color']}{colors[board[row][col][0]]['filler']}{Style.RESET_ALL}"

# i am the thinker
def board_numbers(board):
    adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    # iterate through every board position
    for x in range(board_width):
        for y in range(board_height):
            
            # skip positions with bombs
            if board[y][x][0] == b:
                continue
            
            # counter for adjacent bombs
            adj_bombs = 0
            
            # iterate through the adjacents of each position
            for a in adjacents:
                adj_x, adj_y = x + a[0], y + a[1]
                # ensure that the current adjacent is on the board
                if 0 <= adj_x < board_width and 0 <= adj_y < board_height:
                    # if the adjacent contains a bomb then increase the counter
                    if board[adj_y][adj_x][0] == b:
                        adj_bombs += 1
            
            # update the current position with how many adjacent bombs were counted
            board[y][x][0] = adj_bombs

board_numbers(board)
print_board(board, color=True)