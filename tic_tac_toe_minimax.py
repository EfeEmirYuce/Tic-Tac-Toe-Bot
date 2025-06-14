import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // 3
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw grid lines
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*SQUARE_SIZE), (WIDTH, 2*SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*SQUARE_SIZE, 0), (2*SQUARE_SIZE, HEIGHT), LINE_WIDTH)

draw_lines()

# Draw symbols
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                # Draw cross
                start1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                start2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)
            elif board[row][col] == 'O':
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

# Check winner
def check_win(player):
    # Rows, columns, diagonals
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(BOARD_COLS):
        if [board[row][col] for row in range(BOARD_ROWS)].count(player) == 3:
            return True
    if [board[i][i] for i in range(BOARD_ROWS)].count(player) == 3:
        return True
    if [board[i][BOARD_ROWS - i - 1] for i in range(BOARD_ROWS)].count(player) == 3:
        return True
    return False

def is_board_full():
    return all(all(cell is not None for cell in row) for row in board)

# Minimax algorithm
def minimax(depth, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    score = minimax(depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    score = minimax(depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# AI Move
def ai_move():
    best_score = -math.inf
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 'O'
                score = minimax(0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = 'O'

# Main loop
player_turn = True
game_over = False
winner = None
font = pygame.font.SysFont(None, 60)

def display_result(text):
    result_surf = font.render(text, True, (255, 255, 255))
    rect = result_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(result_surf, rect)
    pygame.display.update()

def reset_game():
    global board, player_turn, game_over, winner
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player_turn = True
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()

reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            if board[row][col] is None:
                board[row][col] = 'X'
                if check_win('X'):
                    game_over = True
                    winner = 'X'
                elif is_board_full():
                    game_over = True
                    winner = 'Draw'
                else:
                    player_turn = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    if not player_turn and not game_over:
        pygame.time.wait(500)  # Delay to simulate thinking
        ai_move()
        if check_win('O'):
            game_over = True
            winner = 'O'
        elif is_board_full():
            game_over = True
            winner = 'Draw'
        else:
            player_turn = True

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()

    if game_over:
        if winner == 'Draw':
            display_result("It's a Draw! Press R to Restart")
        else:
            display_result(f"{winner} Wins! Press R to Restart")

    pygame.display.update()

