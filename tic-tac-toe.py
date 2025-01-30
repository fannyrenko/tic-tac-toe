import pygame as pg
import sys
from pygame.locals import *

# Initialize variables
current_player = 'x'
current_winner = None
is_draw = False
reset_timer = None 

WIDTH = 400
HEIGHT = 400
BACKGROUND = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

grid = [[None] * 3, [None] * 3, [None] * 3]

pg.init()
FPS = 30
clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)  # 400 x 500 display
pg.display.set_caption("Tic Tac Toe")

size = 80  # size of the X / O marks

def game_initiating_window():
    """Initializes game window"""
    screen.fill(BACKGROUND)
    pg.draw.line(screen, LINE_COLOR, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(screen, LINE_COLOR, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)
    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)
    draw_status()

def draw_status():
    """Draws the status bar"""
    global is_draw
    if current_winner is None:
        message = f"{current_player.upper()}'s Turn"
    else:
        message = f"{current_winner.upper()} Won!"
    if is_draw:
        message = "Game Draw!"

    font = pg.font.Font(None, 30)
    text = font.render(message, True, (255, 255, 255))
    screen.fill((0, 0, 0), (0, 400, 500, 100))  # Clear the status bar area
    text_rect = text.get_rect(center=(WIDTH / 2, 450))  # Center text
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    """Checks game grid for wins or draws"""
    global grid, current_winner, is_draw, reset_timer

    # Check rows
    for row in range(3):
        if grid[row][0] == grid[row][1] == grid[row][2] and grid[row][0] is not None:
            current_winner = grid[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6), 4)
            reset_timer = pg.time.get_ticks() 
            return

    # Check columns
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] and grid[0][col] is not None:
            current_winner = grid[0][col]
            pg.draw.line(screen, (250, 0, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)
            reset_timer = pg.time.get_ticks() 
            return

    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] is not None:
        current_winner = grid[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
        reset_timer = pg.time.get_ticks() 
        return

    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] is not None:
        current_winner = grid[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
        reset_timer = pg.time.get_ticks() 
        return

    # Check for draw
    if all(all(row) for row in grid) and current_winner is None:
        is_draw = True
        reset_timer = pg.time.get_ticks() 

    draw_status()

def drawXO(row, col):
    """Draws the X's and O's on the board"""
    global grid, current_player

    pos_x = (col - 1) * (WIDTH // 3) + (WIDTH // 6) - (size // 2)
    pos_y = (row - 1) * (HEIGHT // 3) + (HEIGHT // 6) - (size // 2)

    grid[row - 1][col - 1] = current_player

    if current_player == 'x':
        pg.draw.line(screen, (0, 0, 0), (pos_x, pos_y), (pos_x + size, pos_y + size), 5)
        pg.draw.line(screen, (0, 0, 0), (pos_x, pos_y + size), (pos_x + size, pos_y), 5)
        current_player = 'o'
    else:
        center = (pos_x + size // 2, pos_y + size // 2)
        radius = size // 2 - 5
        pg.draw.circle(screen, (0, 0, 0), center, radius, 5)
        current_player = 'x'

    pg.display.update()

def user_click():
    """Finds the position of the user's click"""
    x, y = pg.mouse.get_pos()
    col = 1 if x < WIDTH / 3 else 2 if x < WIDTH / 3 * 2 else 3
    row = 1 if y < HEIGHT / 3 else 2 if y < HEIGHT / 3 * 2 else 3

    if grid[row - 1][col - 1] is None:
        drawXO(row, col)
        check_win()

def reset_game():
    """Restarts game on win or draw"""
    global grid, current_winner, current_player, is_draw, reset_timer
    current_player = 'x'
    is_draw = False
    current_winner = None
    reset_timer = None  # Reset the timer
    grid = [[None] * 3, [None] * 3, [None] * 3]
    game_initiating_window()

game_initiating_window()

while True:
    for event in pg.event.get():
        if event.type == QUIT: 
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if current_winner or is_draw:
                reset_game()
            else:
                user_click()

    
    # Reset the game after 10 seconds
    if reset_timer is not None and pg.time.get_ticks() - reset_timer > 10000:
        reset_game()

    pg.display.update()
    clock.tick(FPS)
