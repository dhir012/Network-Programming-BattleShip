#Creats a ship, and position on the board
#Manage their states of being hit or sunk
class Ship:
    class Ship:
        def __init__(self, size):
            self.size = size
            self.positions = []  # List of (x, y) coordinates
            self.hits = 0

        def is_sunk(self):
            return self.hits >= self.size

        def add_hit(self):
            self.hits += 1