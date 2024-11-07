#A grid for the Game Board
#Keeps track of the hits and misses
import pygame

class Board:
    def __init__(self):
        self.grid = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]

    def is_empty(self, x, y):
        return self.grid[x][y] == '~'

    def place_ship(self, ship, x, y):
        self.grid[x][y] = 'S'  # 'S' for ship
        ship.positions.append((x, y))

    def process_hit(self, x, y):
        if self.grid[x][y] == 'S':  # Hit a ship
            self.grid[x][y] = 'H'    # 'H' for hit
            return "Hit!"
        elif self.grid[x][y] == '~':  # Missed
            self.grid[x][y] = 'M'    # 'M' for miss
            return "Miss!"
        return "Already attacked here!"

    def display(self):
        # Optional method to display the board for debugging or the UI
        for row in self.grid:
            print(" ".join(row))

if __name__ == "__main__":
    main()