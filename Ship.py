class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = []  # List of tuples indicating ship positions on the grid
        self.hits = 0

    def is_sunk(self):
        return self.hits >= self.size
