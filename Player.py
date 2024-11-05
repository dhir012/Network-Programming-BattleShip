class Player:
    def __init__(self, connection):
        self.connection = connection
        self.grid = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ships = []
        self.remaining_ships = 3

    def place_ships(self):
        # Randomly place 3 single-cell ships
        for _ in range(3):
            ship = Ship(1)
            while True:
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                if self.grid[x][y] == '~':
                    self.grid[x][y] = 'S'
                    ship.positions.append((x, y))
                    break
            self.ships.append(ship)

    def process_hit(self, x, y):
        for ship in self.ships:
            if (x, y) in ship.positions:
                ship.hits += 1
                if ship.is_sunk():
                    self.remaining_ships -= 1
                    return "Hit and sunk!"
                return "Hit!"
        return "Miss!"
