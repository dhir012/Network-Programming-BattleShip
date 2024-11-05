class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = []  # List of tuples indicating ship positions on the grid
        self.hits = 0

    def is_sunk(self):
        return self.hits >= self.size

def place_ship(board, size, start_pos, orientation):
    x, y = start_pos
    coordinates = []

    if orientation == "horizontal":
        for i in range(size):
            coordinates.append((x + i, y))
    elif orientation == "vertical":
        for i in range(size):
            coordinates.append((x, y + i))

    for coord in coordinates:
        if coord[0] < 0 or coord[0] >= BOARD_SIZE or coord[1] < 0 or coord[1] >= BOARD_SIZE:
            raise ValueError("Ship is out of bounds!")
        if board[coord[1]][coord[0]] != 0:
            raise ValueError("Ship is already occupied!")
        board[coord[1]][coord[0]] = 1

    return Ship(size, coordinates)


