from copy import deepcopy
import pygame

# initialize pygame
pygame.init()
clock = pygame.time.Clock()

# set game to bet running (A player may make this false and end the game)
RUNNING = True

# Dimensions of the window
width = 800
height = 800

# Create a font to use to write "X" and "O" on screen
myfont = pygame.font.SysFont('Comic Sans MS', 150, bold=True)

# create a screen with the title "Tic-Tac-Toe"
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")

# Establish first round settings. Next round these will switch
player = "X"
opponent = "O"

# function: creates board made of empty strings


def create_board():
    return [["" for i in range(3)] for i in range(3)]

# function: takes the position of mouse click, finds the accociated cell, and changes it to the player's mark if its not already taken


def play_move(board, mousey, mousex, player):
    for i in (width/3, 2*width/3, width):
        for j in (width/3, 2*width/3, width):
            if mousey < i and mousex < j:
                if board[int(i/width*3-1)][int(j/width*3-1)] == "":
                    board[int(i/width*3-1)][int(j/width*3-1)] = player
                return


def play_move_hard(board, player, row, col):
    board[row][col] = player

# function: Tests if any of the winner possibilities is true and returns the winner, the line/list where they won, and a tag saying the direction of the line


def get_winner(board):
    for player in ["X", "O"]:
        for y in board:
            if all(cell == player for cell in y):
                return player, y, "row"
        for column in get_columns(board):
            if all(cell == player for cell in column):
                return player, column, "col"
        for diagonal in get_diagonals(board):
            if all(cell == player for cell in diagonal):
                return player, diagonal, "diag"
    else:
        return None, None, None

# function: Creates a list of 3 columns


def get_columns(board):
    result = [[y[x_idx] for y in board] for x_idx in range(3)]
    return result

# function: Creates a list of 2 diagnals


def get_diagonals(board):
    diag1 = [board[index][index] for index in range(3)]
    diag2 = [board[row][column] for row, column in enumerate(range(2, -1, -1))]
    return diag1, diag2

# function: tests if there is a winner. If there is, it draws a red line through the line/list of X's or O's where they won


def draw_winner_line(board):
    if get_winner(board)[0] == opponent:
        listline = get_winner(board)[1]
        linetype = get_winner(board)[2]
        if linetype == "row":
            y_coord = ((2*board.index(listline)+1)/6*height)
            pygame.draw.line(screen, (255, 0, 0),
                             (0, y_coord+10), (width, y_coord+10), 5)
        if linetype == "col":
            x_coord = ((2*get_columns(board).index(listline)+1)/6*width)
            pygame.draw.line(screen, (255, 0, 0),
                             (x_coord, 0), (x_coord, height), 10)
        if linetype == "diag":
            x_coord1 = ((4*get_diagonals(board).index(listline)+1)/6*height)
            x_coord2 = (
                1 - ((4*get_diagonals(board).index(listline)+1)/6))*height
            pygame.draw.line(screen, (255, 0, 0), (x_coord1,
                                                   width/6), (x_coord2, 5*width/6), 10)

# function: creates the white grid lines of the Tix-Tac-Toe board


def create_grid_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, (255, 255, 255),
                         (i*width/3-5, 0), (i*width/3-5, height), 10)
        pygame.draw.line(screen, (255, 255, 255),
                         (0, i*height/3-5), (width, i*height/3-5), 10)

# function: for each cell, display on the screen the player who has that cell


def fill_in_cells(board):
    for i in range(3):
        for j in range(3):
            cell_block = myfont.render(board[i][j], False, (255, 255, 255))
            screen.blit(cell_block, ((j*2+1)/6*width-60, (i*2+1)/6*height-100))


# create the board
board = create_board()

# run the game

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if get_winner(board)[0] == None:
                mousex, mousey = pygame.mouse.get_pos()
                play_move(board, mousey, mousex, player)

                # switches the player and opponent X/O roles
                player, opponent = opponent, player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board = create_board()
                player, opponent = "X", "O"

    screen.fill((100, 100, 100))

    create_grid_lines()
    fill_in_cells(board)

    draw_winner_line(board)

    clock.tick(60)
    pygame.display.flip()

