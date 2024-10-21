import random
from colorama import Fore, Style

def print_board_raw(board):
    for row in board:
        print(row)

def print_board(board):
    for row in board:
        for col in row:
            print(col, end=' ')
        print()

rows = 9
cols = 9
num_bombs = 10



board = [["0" for _ in range(cols)] for _ in range(rows)]

def get_random_coordinate(rows, cols):
    x = random.randint(0, rows-1)
    y = random.randint(0, cols-1)

    return x, y

print_board(board)

for i in range(num_bombs):
    bomb_x, bomb_y = get_random_coordinate(rows, cols)
    # while board[bomb_x][bomb_y] != -1:
    #     bomb_x, bomb_y = get_random_coordinate(rows, cols)
    board[bomb_x][bomb_y] = f"{Fore.RED}9{Style.RESET_ALL}"
    print(f"Placed a bomb at ({bomb_x}, {bomb_y})")

# print_board(board)

# for row in range(len(board)):
#     for col in range(len(board[row])):
#         if board[row][col] == 9: continue
#         adjacent_bombs = 0
#         if row-1 >= 0:
#             adjacent_bombs += [board[row-1][col-1:col+2]].count(9)
#         if row+1 <= len(board)-1:
#             adjacent_bombs += [board[row+1][col-1:col+2]].count(9)
#         if col-1 >= 0:
#             adjacent_bombs += [board[row][col-1]].count(9)
#         if col+1 <= len(board[row])-1:
#             adjacent_bombs += [board[row][col+1]].count(9)
#         board[row][col] = adjacent_bombs
            
print_board(board)


# for x in range(len(boad)):
#     for y in range(len(x)):
#         if boad[x][y] == c:
#             x-1[y-1:y+1]

