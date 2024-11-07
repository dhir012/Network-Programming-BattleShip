#Will be the function where it handles the game logic
import pygame

from GameState import draw_game_state
from PlayerToAttack import attack
from Ship import place_ship
from server import CELL_SIZE, BOARD_SIZE


def main():
    # Create empty boards (0: empty, 1: ship, 2: hit, 3: miss)
    # Place ships on the boards (for now, we'll hard-code ship placements)
    # Player starts the game
    # Player attacks the opponent's board
    # Opponent attacks the player's board (AI logic or player action)

    pygame.quit()

if __name__ == "__main__":
    main()