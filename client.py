import socket
import pygame
import threading
import sys

# Network
HOST = '127.0.0.1'
PORT = 12345

# creates client socket and tries connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Could not connect to the server. Ensure the server is running.")
    sys.exit()

# pygame setup
pygame.init()
CELL_SIZE = 40  # size of each cell
GRID_SIZE = 10  # number of cells in grid (10x10)
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE * 2 + 60
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + 100
BACKGROUND_COLOR = (30, 30, 60)
WHITE = (255, 255, 255)
WATER_COLOR = (173, 216, 230)
SHIP_COLOR = (105, 105, 105)
HIT_COLOR = (255, 69, 0)
MISS_COLOR = (135, 206, 250)
GRID_BORDER_COLOR = (0, 0, 0)
PREVIEW_COLOR = (144, 238, 144)

# create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Networked Battleship")

# initialize game boards
player_board = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
opponent_board = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]

# game state
player_turn = False # indicates player turns
placing_ships = True  # indicates if player is in ship placement phase
current_ship_size = 5  # largest ship size
ships_to_place = [5, 4, 3, 3, 2]  # ships
player_id = -1  # ID of player (server sets)
winner = None
preview_position = None  # current mouse position
orientation = 'horizontal'  # ship orientation

# draw board on screen
def draw_board(board, offset_x=0, is_opponent=False):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WATER_COLOR
            if board[y][x] == 'H':
                color = HIT_COLOR  # hit cells
            elif board[y][x] == 'M':
                color = MISS_COLOR  # missed cells
            elif board[y][x] == 'S' and not is_opponent:
                color = SHIP_COLOR  # ship cells

            rect = pygame.Rect(x * CELL_SIZE + offset_x, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_BORDER_COLOR, rect, 1)

# for preview of the ship before placing it
def draw_preview(x, y, size, orientation):
    valid = True  # if ship is able to be placed

    # if placement is valid and draws preview
    if orientation == 'horizontal':
        if x + size <= GRID_SIZE:
            for i in range(size):
                if player_board[y][x + i] != '~':  # if space is occupied
                    valid = False
                    break
        else:
            valid = False  # oob horizontaly
    elif orientation == 'vertical':
        if y + size <= GRID_SIZE:
            for i in range(size):
                if player_board[y + i][x] != '~':
                    valid = False
                    break
        else:
            valid = False  # oob vertically

    # draw preview only if position is valid
    if valid:
        for i in range(size):
            if orientation == 'horizontal':
                rect = pygame.Rect((x + i) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            else:
                rect = pygame.Rect(x * CELL_SIZE, (y + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, PREVIEW_COLOR, rect)
            pygame.draw.rect(screen, GRID_BORDER_COLOR, rect, 1)

    return valid

# place a ship on player board
def place_ship(x, y, size, orientation):
    if orientation == 'horizontal' and x + size <= GRID_SIZE:
        if all(player_board[y][x + i] == '~' for i in range(size)):
            for i in range(size):
                player_board[y][x + i] = 'S'
            return True
    elif orientation == 'vertical' and y + size <= GRID_SIZE:
        if all(player_board[y + i][x] == '~' for i in range(size)):
            for i in range(size):
                player_board[y + i][x] = 'S'
            return True
    return False

# sends move to server
def send_move(x, y):
    client.send(f"MOVE:{x},{y}".encode())

# main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_board(player_board, offset_x=0)
    draw_board(opponent_board, offset_x=GRID_SIZE * CELL_SIZE + 20, is_opponent=True)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            client.close()  # close client connection
            sys.exit()

        # handles ship placement preview
        elif placing_ships and event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                preview_position = (grid_x, grid_y)

        # handles ship placement on click
        elif placing_ships and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and preview_position:  # Left mouse button
                grid_x, grid_y = preview_position
                if draw_preview(grid_x, grid_y, current_ship_size, orientation) and place_ship(grid_x, grid_y, current_ship_size, orientation):
                    ships_to_place.pop(0)  # Remove placed ship size from list
                    current_ship_size = ships_to_place[0] if ships_to_place else 0
                    if not ships_to_place:  # All ships placed
                        placing_ships = False
                        client.send("PLACEMENT_DONE".encode())  # notify server

        # handles rotating ships
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                orientation = 'vertical' if orientation == 'horizontal' else 'horizontal'

        # handles players move
        elif player_turn and not placing_ships and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                x, y = pygame.mouse.get_pos()
                grid_x = (x - GRID_SIZE * CELL_SIZE - 20) // CELL_SIZE
                grid_y = y // CELL_SIZE
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    send_move(grid_x, grid_y)
                    player_turn = False  # end turn

    # draw ship placement if able to
    if preview_position and placing_ships:
        draw_preview(preview_position[0], preview_position[1], current_ship_size, orientation)

    # instructions
    if placing_ships:
        instructions = f"Place your ship of size {current_ship_size}. Press 'R' to rotate. Click to confirm."
        text_surface = pygame.font.Font(None, 24).render(instructions, True, WHITE)
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 90))

    # display winner
    if winner:
        text_surface = pygame.font.Font(None, 36).render(f"{winner} wins!", True, WHITE)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False

    pygame.display.flip()  # update display

pygame.quit()