import pygame
import random
from colorama import Fore, Style, init

# initialize pygame and colorama
pygame.init()
init(autoreset=True)

# define constants
board_width = 30
board_height = 16
num_bombs = 99
tile_size = 30  # size of each tile in pixels
b = 9

# colors for terminal
terminal_colors = {
    9: {'filler': 'B', 'color': Fore.RED},
    1: {'filler': '1', 'color': Fore.LIGHTBLUE_EX},
    2: {'filler': '2', 'color': Fore.GREEN},
    3: {'filler': '3', 'color': Fore.YELLOW},
    4: {'filler': '4', 'color': Fore.BLUE},
    5: {'filler': '5', 'color': Fore.RED},
    6: {'filler': '6', 'color': Fore.CYAN},
    7: {'filler': '7', 'color': Fore.MAGENTA},
    8: {'filler': '8', 'color': Fore.YELLOW},
    0: {'filler': '-', 'color': Fore.WHITE},
    'F': {'filler': 'F', 'color': Fore.LIGHTGREEN_EX},
    '?': {'filler': '?', 'color': Fore.LIGHTBLACK_EX},
}

# colors for pygame
colors = {
    9: pygame.Color("red"),
    1: pygame.Color("lightblue"),
    2: pygame.Color("green"),
    3: pygame.Color("yellow"),
    4: pygame.Color("blue"),
    5: pygame.Color("red"),
    6: pygame.Color("cyan"),
    7: pygame.Color("magenta"),
    8: pygame.Color("orange"),
    0: pygame.Color("grey"),
}

# initialize the screen for pygame
screen = pygame.display.set_mode((board_width * tile_size, board_height * tile_size))
pygame.display.set_caption("Minesweeper")

# load the image (tackle box cat)
image = pygame.image.load('image.png')  # Load the image
image_width, image_height = 300, 300  # Desired width and height for the image
image = pygame.transform.scale(image, (image_width, image_height))  # Optionally scale the image

# initial position and velocity for the bouncing image
image_x = 0
image_y = 0
image_x_velocity = 1  # Adjust the velocity as needed
image_y_velocity = 1

# create the board
key = {"value": 0, "visibility": 0, "flagged": False}  # adding "flagged" to store flagged status
board = [[[attribute for attribute in key.values()] for _ in range(board_width)] for _ in range(board_height)]

bomb_positions = random.sample(range(board_height * board_width), num_bombs)

# place bombs on the board
for pos in bomb_positions:
    board[pos // board_width][pos % board_width][0] = b

# calculate adjacent bomb numbers
def board_numbers(board):
    adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for x in range(board_width):
        for y in range(board_height):
            if board[y][x][0] == b:
                continue
            
            adj_bombs = 0
            for a in adjacents:
                adj_x, adj_y = x + a[0], y + a[1]
                if 0 <= adj_x < board_width and 0 <= adj_y < board_height:
                    if board[adj_y][adj_x][0] == b:
                        adj_bombs += 1
            board[y][x][0] = adj_bombs

board_numbers(board)

# function to reveal cascading empty tiles
def cascade_reveal(row, col):
    if board[row][col][1] == 1:  # already revealed, skip
        return
    
    board[row][col][1] = 1  # reveal the tile
    if board[row][col][0] == 0:  # if it's an empty tile, continue cascading
        adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for a in adjacents:
            adj_x, adj_y = col + a[0], row + a[1]
            if 0 <= adj_x < board_width and 0 <= adj_y < board_height:
                cascade_reveal(adj_y, adj_x)

# function to print the entire board to the terminal with color (all tiles visible)
def print_full_board(board):
    for row in board:
        row_repr = []
        for col in row:
            if col[2]:  # flagged tile
                row_repr.append(f"{terminal_colors['F']['color']}{terminal_colors['F']['filler']}{Style.RESET_ALL}")
            else:
                if col[0] == b:
                    row_repr.append(f"{terminal_colors[9]['color']}{terminal_colors[9]['filler']}{Style.RESET_ALL}")
                else:
                    row_repr.append(f"{terminal_colors[col[0]]['color']}{terminal_colors[col[0]]['filler']}{Style.RESET_ALL}")
        print(" ".join(row_repr))
    print()  # extra newline for spacing

# main game loop
running = True
font = pygame.font.SysFont(None, 25)

def draw_board():
    for row in range(board_height):
        for col in range(board_width):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)  # draw the border

            # check if the tile is flagged
            if board[row][col][2] == True:
                pygame.draw.rect(screen, (255, 255, 0), rect)  # draw flagged tile in yellow
                text = font.render("F", True, pygame.Color("black"))
                screen.blit(text, (col * tile_size + 10, row * tile_size + 5))  # render flag

            # reveal the tile if it's visible
            elif board[row][col][1] == 1:
                if board[row][col][0] == b:
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # bomb tile is red
                    text = font.render("B", True, pygame.Color("black"))
                else:
                    pygame.draw.rect(screen, (100, 100, 100), rect)  # revealed tile is grey
                    text = font.render(str(board[row][col][0]), True, colors[board[row][col][0]])

                screen.blit(text, (col * tile_size + 10, row * tile_size + 5))  # place the number/bomb on the tile

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            col = mouse_pos[0] // tile_size
            row = mouse_pos[1] // tile_size

            if event.button == 1 and not board[row][col][2]:  # left-click to reveal a tile (if not flagged)
                if board[row][col][0] == 0:
                    cascade_reveal(row, col)  # cascade if it's an empty tile
                else:
                    board[row][col][1] = 1  # make the tile visible
                print_full_board(board)  # print the entire game board after left-click

            elif event.button == 3:  # right-click to flag/unflag a tile
                if not board[row][col][1]:  # don't flag if the tile is revealed
                    board[row][col][2] = not board[row][col][2]  # toggle flag status
                print_full_board(board)  # print the entire game board after right-click

    # update the image position
    image_x += image_x_velocity
    image_y += image_y_velocity

    # check for boundary collisions and reverse velocity to "bounce"
    if image_x <= 0 or image_x + image_width >= board_width * tile_size:
        image_x_velocity = -image_x_velocity
    if image_y <= 0 or image_y + image_height >= board_height * tile_size:
        image_y_velocity = -image_y_velocity

    # draw the bouncing image on the screen
    screen.blit(image, (image_x, image_y))

    # draw the board every frame
    draw_board()

    pygame.display.flip()  # update the screen

pygame.quit()
