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
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)

# Initialize the game board
board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

board_width = COLUMNS * SQUARE_SIZE
board_start_x = (WINDOW_WIDTH - board_width) // 2

# Initialize the window and font
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Connect Four")
myfont = pygame.font.Font(pygame.font.get_default_font(), 75)
small_font = pygame.font.Font(pygame.font.get_default_font(), 30)

def draw_board():
    screen.fill(DARK_GRAY)

    board_width = COLUMNS * SQUARE_SIZE
    board_height = ROWS * SQUARE_SIZE
    board_start_x = (WINDOW_WIDTH - board_width) // 2
    board_start_y = (WINDOW_HEIGHT - board_height) // 2

    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, WHITE, (board_start_x + col * SQUARE_SIZE, board_start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
            pygame.draw.circle(screen, BLACK, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_start_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CORAL, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, MEDIUM_TURQUOISE, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    pygame.display.update()

# ... previous code with draw_board function ...
board_start_y = (WINDOW_HEIGHT - (ROWS * SQUARE_SIZE)) // 2


def animate_drop(col, row, color):
    for i in range(ROWS - 1, row - 1, -1):
        if i != ROWS - 1:  # Don't draw a black circle for the first iteration
            pygame.draw.circle(screen, BLACK, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                               board_start_y + (ROWS - i - 2) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

        pygame.draw.circle(screen, color, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                           board_start_y + (ROWS - i - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
        pygame.display.update()
        pygame.time.delay(30)

    pygame.draw.circle(screen, color, (board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                       board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)


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
    message = small_font.render("Press Y to play again or N to quit.", 1, WHITE)
    message_x = (WINDOW_WIDTH - message.get_width()) // 2
    message_y = (WINDOW_HEIGHT - message.get_height()) // 2
    screen.fill(DARK_GRAY)
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
                animate_drop(col, row, CORAL if turn % 2 == 0 else MEDIUM_TURQUOISE)

                if check_winner(turn % 2 + 1):
                    draw_board()
                    winning_color = CORAL if turn % 2 == 0 else MEDIUM_TURQUOISE
                    label = myfont.render(f"Player {turn % 2 + 1} wins!", 1, winning_color)
                    label_width = label.get_width()
                    label_height = label.get_height()
                    label_x = (WINDOW_WIDTH - label_width) // 2
                    label_y = (WINDOW_HEIGHT - label_height) // 2
                    padding = 20
                    pygame.draw.rect(screen, (128, 128, 128), (
                    label_x - padding, label_y - padding, label_width + 2 * padding, label_height + 2 * padding))
                    screen.blit(label, (label_x, label_y))
                    pygame.display.update()
                    pygame.time.delay(3000)  # Add a delay (in milliseconds) before showing the play again screen

                    if show_play_again_screen():
                        board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
                        game_over = False
                        turn = 0
                    else:
                        pygame.quit()
                        sys.exit()

                turn += 1
                draw_board()
