import pygame
import pygame.gfxdraw

BOARD_SIZE = 10
Cell_SIzE = 50
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BattleShip Game")

def draw_grid():
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, BOARD_SIZE * CELL_SIZE))
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (BOARD_SIZE * CELL_SIZE, CELL_SIZE * i))

        def draw_board():
            screen.fill(WHITE)
            draw_grid()
            pygame.display.flip()
        def main():
            draw_board()

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        if event.key == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
            pygame.quit()

if __name__ == '__main__':
    main()