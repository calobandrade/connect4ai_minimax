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


class Connect4:
    board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

    def __init__(self):
        self.turn = 0
        self.game_over = False

        # Initialize the window and font
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect Four")
        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 75)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), 30)

        self.board_start_x = (WINDOW_WIDTH - COLUMNS * SQUARE_SIZE) // 2
        self.board_start_y = (WINDOW_HEIGHT - ROWS * SQUARE_SIZE) // 2

        # Initialize the AI
        self.ai = MinMaxAI(depth=5, connect4=self)

    @classmethod
    def is_valid_location(cls, col):
        return cls.board[ROWS-1][col] == 0

    @classmethod
    def get_next_open_row(cls, col):
        for row in range(ROWS):
            if cls.board[row][col] == 0:
                return row

    @classmethod
    def drop_piece(cls, row, col, piece):
        cls.board[row][col] = piece

    def __init__(self):
        self.turn = 0
        self.game_over = False

        # Initialize the window and font
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Connect Four")
        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 75)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), 30)

        self.board_start_x = (WINDOW_WIDTH - COLUMNS * SQUARE_SIZE) // 2
        self.board_start_y = (WINDOW_HEIGHT - ROWS * SQUARE_SIZE) // 2

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                col = (event.pos[0] - self.board_start_x) // SQUARE_SIZE
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    self.drop_piece(row, col, self.turn % 2 + 1)
                    self.animate_drop(col, row, CORAL if self.turn % 2 == 0 else MEDIUM_TURQUOISE)

                    if self.check_winner(self.turn % 2 + 1):
                        self.draw_board()
                        winning_color = CORAL if self.turn % 2 == 0 else MEDIUM_TURQUOISE
                        label = self.myfont.render(f"Player {self.turn % 2 + 1} wins!", 1, winning_color)
                        label_width = label.get_width()
                        label_height = label.get_height()
                        label_x = (WINDOW_WIDTH - label_width) // 2
                        label_y = (WINDOW_HEIGHT - label_height) // 2
                        padding = 20
                        pygame.draw.rect(self.screen, (128, 128, 128), (
                            label_x - padding, label_y - padding, label_width + 2 * padding,
                            label_height + 2 * padding))
                        self.screen.blit(label, (label_x, label_y))
                        pygame.display.update()
                        pygame.time.delay(3000)  # Add a delay (in milliseconds) before showing the play again screen

                        if self.show_play_again_screen():
                            self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
                            self.game_over = False
                            self.turn = 0
                        else:
                            self.game_over = True

                    self.turn += 1
                    self.draw_board()

            if self.turn % 2 == 1 and not self.game_over:
                ai = MinMaxAI(depth=5)  # Initialize the AI with a search depth of 5
                col = ai.get_best_move(self.board, maximizing_player=True)
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, self.turn % 2 + 1)
                self.animate_drop(col, row, CORAL if self.turn % 2 == 0 else MEDIUM_TURQUOISE)

                if self.check_winner(self.turn % 2 + 1):
                    self.draw_board()
                    winning_color = CORAL if self.turn % 2 == 0 else MEDIUM_TURQUOISE
                    label = self.myfont.render(f"Player {self.turn % 2 + 1} wins!", 1, winning_color)
                    label_width = label.get_width()
                    label_height = label.get_height()
                    label_x = (WINDOW_WIDTH - label_width) // 2
                    label_y = (WINDOW_HEIGHT - label_height) // 2
                    padding = 20
                    pygame.draw.rect(self.screen, (128, 128, 128), (
                        label_x - padding, label_y - padding, label_width + 2 * padding,
                        label_height + 2 * padding))
                    self.screen.blit(label, (label_x, label_y))
                    pygame.display.update()
                    pygame.time.delay(3000)  # Add a delay (in milliseconds) before showing the play again screen

                    if self.show_play_again_screen():
                        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
                        self.game_over = False
                        self.turn = 0
                    else:
                        self.game_over = True

                self.turn += 1
                self.draw_board()

        if self.turn % 2 == 1 and not self.game_over:
            ai = MinMaxAI(depth=5)  # Initialize the AI with a search depth of 5
            col = ai.get_best_move(self.board, maximizing_player=True)
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.turn % 2 + 1)
            self.animate_drop(col, row, CORAL if self.turn % 2 == 0 else MEDIUM_TURQUOISE)

    # Game over
    pygame.quit()
    sys.exit()

    def draw_board(self):
        self.screen.fill(DARK_GRAY)

        for row in range(ROWS):
            for col in range(COLUMNS):
                pygame.draw.rect(self.screen, WHITE, (
                self.board_start_x + col * SQUARE_SIZE, self.board_start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                                 2)
                pygame.draw.circle(self.screen, BLACK, (
                self.board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                self.board_start_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, CORAL, (
                    self.board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    self.board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
                elif self.board[row][col] == 2:
                    pygame.draw.circle(self.screen, MEDIUM_TURQUOISE, (
                    self.board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    self.board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

        pygame.display.update()

    def is_valid_location(self, col):
        return self.board[ROWS-1][col] == 0

    def get_next_open_row(self, col):
        for row in range(ROWS):
            if self.board[row][col] == 0:
                return row

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def check_winner(self, piece):
        # Horizontal
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row][col+i] == piece for i in range(4)):
                    return True

        # Vertical
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if all(self.board[row+i][col] == piece for i in range(4)):
                    return True

        # Positive Diagonal
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row+i][col+i] == piece for i in range(4)):
                    return True

        # Negative Diagonal
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row-i][col+i] == piece for i in range(4)):
                    return True

    def show_play_again_screen(self):
        message = self.small_font.render("Press Y to play again or N to quit.", 1, WHITE)
        message_x = (WINDOW_WIDTH - message.get_width()) // 2
        message_y = (WINDOW_HEIGHT - message.get_height()) // 2
        self.screen.fill(DARK_GRAY)
        self.screen.blit(message, (message_x, message_y))
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

    def animate_drop(self, col, row, color):
        for i in range(ROWS - 1, row - 1, -1):
            if i != ROWS - 1:  # Don't draw a black circle for the first iteration
                pygame.draw.circle(self.screen, BLACK, (self.board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                               self.board_start_y + (ROWS - i - 2) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

            pygame.draw.circle(self.screen, color, (self.board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                           self.board_start_y + (ROWS - i - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            pygame.display.update()
            pygame.time.wait(30)

        pygame.draw.circle(self.screen, color, (self.board_start_x + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                       self.board_start_y + (ROWS - row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    def run_game(self):
        self.draw_board()  # Draw the board initially
        while not self.game_over:
            self.update()

        # Keep the game running until the player chooses to quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


class MinMaxAI:
    def __init__(self, depth, connect4):
        self.depth = depth
        self.connect4 = connect4

    def get_best_move(self, board, maximizing_player):
        best_score = -float('inf') if maximizing_player else float('inf')
        best_col = None

        for col in range(COLUMNS):
            if not self.connect4.is_valid_location(col):
                continue

            row = self.connect4.get_next_open_row(col)
            new_board = [row[:] for row in board]
            self.connect4.drop_piece(new_board, row, col, maximizing_player)

            if self.connect4.is_terminal_node(new_board) or self.depth == 0:
                score = self.connect4.evaluate_board(new_board)
            else:
                score = self.minimax(new_board, self.depth - 1, not maximizing_player, -float('inf'), float('inf'))

            if maximizing_player and score > best_score:
                best_score = score
                best_col = col
            elif not maximizing_player and score < best_score:
                best_score = score
                best_col = col

        return best_col

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.connect4.is_terminal_node(board):
            return self.connect4.evaluate_board(board)

        if maximizing_player:
            max_score = -float('inf')
            for col in range(COLUMNS):
                if not self.connect4.is_valid_location(col):
                    continue

                row = self.connect4.get_next_open_row(board, col)
                new_board = [row[:] for row in board]
                self.connect4.drop_piece(new_board, row, col, maximizing_player)
                score = self.minimax(new_board, depth - 1, False, alpha, beta)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for col in range(COLUMNS):
                if not self.connect4.is_valid_location(col):
                    continue

                row = self.connect4.get_next_open_row(board, col)
                new_board = [row[:] for row in board]
                self.connect4.drop_piece(new_board, row, col, maximizing_player)
                score = self.minimax(new_board, depth - 1, True, alpha, beta)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score




if __name__ == '__main__':
    connect4 = Connect4()
    connect4.run_game()
