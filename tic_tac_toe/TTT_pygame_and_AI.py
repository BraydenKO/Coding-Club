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
                    return True
                else:
                    return False


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


# minimax algorithm:
# expand all possibilities
# at end, label a score
# alternate between choosing min and max
# play the max move

def is_still_playing(board: [[str]]) -> bool:
    return len(get_blanks(board)) > 0


def get_blanks(board):
    return [
        (row, column)
        for row in range(3)
        for column in range(3)
        if (board[row][column] == "")
    ]

# output: -1,0,1
# input: the board in that current depth, turn


def minimax(board: [[str]], player: str, turn: str) -> int:
    winner = get_winner(board)[0]
    if winner is not None:
        if winner == player:
            return 1
        else:
            return -1
    else:  # draw/recursive case
        if not is_still_playing(board):
            return 0
        else:
            function = max if player == turn else min
            next_player = "X" if turn == "O" else "O"
            best_score = None
            for (row, column) in get_blanks(board):

                new_board = deepcopy(board)
                new_board[row][column] = turn

                score = minimax(new_board, player, next_player)

                if ((function is max and score == 1) or (function is min and score == -1)):
                    return score
                elif best_score is None:
                    best_score = score
                else:
                    best_score = function(best_score, score)

            return best_score


def print_board(board):
    print("---")
    for row in board:
        for col in row:
            print(col, end=" ")
        print()

# Not currently used


def play_self(board, player, next_player):
    if get_winner(board)[0] != None:
        print("Done")
        return
    for (row, column) in get_blanks(board):
        new_board = deepcopy(board)
        new_board[row][column] = "X"
        score = minimax(new_board, "X", "O")

        if score == 1:
            play_move_hard(board, player, row, column)
            print_board(board)
            play_self(board, next_player, player)
            break


def minimax_part1(board, opponent, player,topscore):
    for (row, column) in get_blanks(board):
        new_board = deepcopy(board)
        new_board[row][column] = opponent
        score = minimax(new_board, opponent, player)
        if score == topscore:
            play_move_hard(board, opponent, row, column)
            print("good")
            break
    else:
        print("less expectation")
        minimax_part1(board, opponent, player,topscore-1)

# create the board
board = create_board()
round = 0
# run the game

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if get_winner(board)[0] == None:
                mousex, mousey = pygame.mouse.get_pos()
                valid = play_move(board, mousey, mousex, player)

                if valid == True and is_still_playing(board) == True:
                    minimax_part1(board,opponent,player,1)
                    valid = None

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
