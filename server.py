#Sets up the Battleship grid/Game Board
import pygame
import pygame.gfxdraw

# Define constants for the game
BOARD_SIZE = 10
CELL_SIZE = 50
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BattleShip Game")

# Function to draw the grid
def draw_grid():
    # Draw horizontal lines
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, BOARD_SIZE * CELL_SIZE))
    # Draw vertical lines
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (BOARD_SIZE * CELL_SIZE, CELL_SIZE * i))

# Function to render the board for a player
def draw_board():
    screen.fill(WHITE)  # Fill the screen with white
    draw_grid()  # Draw the grid on the screen
    pygame.display.flip()

def main():
    draw_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()