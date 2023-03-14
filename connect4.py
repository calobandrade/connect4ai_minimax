!pip install pygame

import pygame
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ROWS = 6
COLUMNS = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

CORAL = (255, 127, 80)
MEDIUM_TURQUOISE = (72, 209, 204)
BLACK = (0, 0, 0)

# Initialize the game board
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

board_width = COLUMNS * SQUARE_SIZE
board_start_x = (WINDOW_WIDTH - board_width) // 2

# Initialize the window and font
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Connect Four")
myfont = pygame.font.SysFont("monospace", 75)

def draw_board():
    screen.fill(BLACK)

    board_width = COLUMNS * SQUARE_SIZE
    board_height = ROWS * SQUARE_SIZE
    board_start_x = (WINDOW_WIDTH - board_width) // 2
    board_start_y = (WINDOW_HEIGHT - board_height) // 2

    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, (255, 255, 255), (board_start_x + col * SQUARE_SIZE, board_start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_start_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CORAL, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, MEDIUM_TURQUOISE, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    pygame.display.update()

def is_valid_location(col):
    return board[ROWS-1][col] == 0

def get_next_open_row(col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row

def drop_piece(row, col, piece):
    board[row][col] = piece

def check_winner(piece):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == piece for i in range(4)):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row+i][col] == piece for i in range(4)):
                return True

    # Positive Diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True

    # Negative Diagonal
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == piece for i in range(4)):
                return True
            
def show_play_again_screen():
    message_font = pygame.font.SysFont("monospace", 30)
    message = message_font.render("Press Y to play again or N to quit.", 1, (255, 255, 255))
    message_x = (WINDOW_WIDTH - message.get_width()) // 2
    message_y = (WINDOW_HEIGHT - message.get_height()) // 2
    screen.fill((0, 0, 0))
    screen.blit(message, (message_x, message_y))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False
# Other functions (is_valid_location, get_next_open_row, drop_piece, check_winner, show_play_again_screen)

turn = 0
game_over = False
draw_board()


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            col = (event.pos[0] - board_start_x) // SQUARE_SIZE
            if is_valid_location(col):
                row = get_next_open_row(col)
                drop_piece(row, col, turn % 2 + 1)

                if check_winner(turn % 2 + 1):
                    draw_board()
                    winning_color = CORAL if turn % 2 == 0 else MEDIUM_TURQUOISE
                    label = myfont.render(f"Player {turn % 2 + 1} wins!", 1, winning_color)
                    label_width = label.get_width()
                    label_height = label.get_height()
                    label_x = (WINDOW_WIDTH - label_width) // 2
                    label_y = (WINDOW_HEIGHT - label_height) // 2
                    pygame.draw.rect(screen, (128, 128, 128), (label_x - 20, label_y - 20, label_width + 40, label_height + 40))
                    screen.blit(label, (label_x, label_y))
                    pygame.display.update()
                    if show_play_again_screen():
                        board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
                        game_over = False
                        turn = 0
                    else:
                        pygame.quit()
                        sys.exit()

                turn += 1
                draw_board()
