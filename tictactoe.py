import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
GRID_SIZE = 3
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
PLAYER_X = 1
PLAYER_O = -1
EMPTY = 0

# Initialize the game board
grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Initialize the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Font
font = pygame.font.Font(None, 36)

# Define the winning combinations
WINNING_COMBINATIONS = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]

# Function to draw the grid
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * GRID_HEIGHT), (WIDTH, row * GRID_HEIGHT), 1)
        pygame.draw.line(screen, LINE_COLOR, (row * GRID_WIDTH, 0), (row * GRID_WIDTH, HEIGHT), 1)

# Function to draw X and O on the board
def draw_xo():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == PLAYER_X:
                x = col * GRID_WIDTH + GRID_WIDTH // 2
                y = row * GRID_HEIGHT + GRID_HEIGHT // 2
                pygame.draw.line(screen, LINE_COLOR, (x - 30, y - 30), (x + 30, y + 30), 2)
                pygame.draw.line(screen, LINE_COLOR, (x + 30, y - 30), (x - 30, y + 30), 2)
            elif grid[row][col] == PLAYER_O:
                x = col * GRID_WIDTH + GRID_WIDTH // 2
                y = row * GRID_HEIGHT + GRID_HEIGHT // 2
                pygame.draw.circle(screen, LINE_COLOR, (x, y), 30, 2)

# Function to check for a win
def check_win(player):
    for combo in WINNING_COMBINATIONS:
        if grid[combo[0] // GRID_SIZE][combo[0] % GRID_SIZE] == player and \
           grid[combo[1] // GRID_SIZE][combo[1] % GRID_SIZE] == player and \
           grid[combo[2] // GRID_SIZE][combo[2] % GRID_SIZE] == player:
            return True
    return False

# Function to check for a draw
def check_draw():
    return all(cell != EMPTY for row in grid for cell in row)

# Function to make a player's move
def player_move(row, col, player):
    if grid[row][col] == EMPTY:
        grid[row][col] = player
        return True
    return False

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(PLAYER_X):
        return -1
    if check_win(PLAYER_O):
        return 1
    if check_draw():
        return 0

    if is_maximizing:
        best_score = float("-inf")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_O
                    score = minimax(board, depth + 1, False)
                    board[row][col] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    score = minimax(board, depth + 1, True)
                    board[row][col] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# Function for AI's move
def ai_move():
    best_score = float("-inf")
    best_move = None

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == EMPTY:
                grid[row][col] = PLAYER_O
                score = minimax(grid, 0, False)
                grid[row][col] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        grid[best_move[0]][best_move[1]] = PLAYER_O
# Main game loop
turn = PLAYER_X
game_over = False
winner = None  # Variable to store the winner
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if turn == PLAYER_X:
            # Player's turn
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // GRID_HEIGHT
                col = x // GRID_WIDTH
                if player_move(row, col, PLAYER_X):
                    turn = PLAYER_O

        elif turn == PLAYER_O:
            # AI's turn
            ai_move()
            turn = PLAYER_X

        screen.fill(WHITE)
        draw_grid()
        draw_xo()

        if check_win(PLAYER_X):
            game_over = True
            winner = "Player X"
        elif check_win(PLAYER_O):
            game_over = True
            winner = "Player O (AI)"
        elif check_draw():
            game_over = True
            winner = "It's a draw!"

        pygame.display.flip()

# Display the result
if winner:
    result_text = font.render(f"{winner} wins!", True, LINE_COLOR)
else:
    result_text = font.render("It's a draw!", True, LINE_COLOR)

screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - result_text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(5000)  
pygame.quit()
sys.exit()
