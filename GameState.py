#Has a Turn-based System function, Handles input, and Game state
import pygame

from PlayerToAttack import attack
from Ship import place_ship
from server import BOARD_SIZE


def draw_game_state(player_board, opponent_board, param, param1):
    pass


def main(CELL_SIZE=None):
    # Create empty boards (0: empty, 1: ship, 2: hit, 3: miss)
    player_board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    opponent_board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Place ships on the boards (for now, we'll hard-code ship placements)
    try:
        place_ship(player_board, 3, (1, 1), "horizontal")
        place_ship(opponent_board, 3, (4, 4), "vertical")
    except ValueError as e:
        print(f"Error placing ship: {e}")

    running = True
    turn = "player"  # Player starts the game
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == "player":
                # Player attacks the opponent's board
                x, y = event.pos
                x //= CELL_SIZE
                y //= CELL_SIZE

                if opponent_board[y][x] == 0 or opponent_board[y][x] == 1:
                    hit = attack(opponent_board, x, y)
                    print(f"Player attacks ({x}, {y}) - {'Hit' if hit else 'Miss'}")
                    turn = "opponent"

            elif event.type == pygame.MOUSEBUTTONDOWN and turn == "opponent":
                # Opponent attacks the player's board (AI logic or player action)
                x, y = event.pos
                x //= CELL_SIZE
                y //= CELL_SIZE
                hit = attack(player_board, x, y)
                print(f"Opponent attacks ({x}, {y}) - {'Hit' if hit else 'Miss'}")
                turn = "player"

        draw_game_state(player_board, opponent_board, [], [])  # Draw the updated game state

    pygame.quit()

if __name__ == "__main__":
    main()