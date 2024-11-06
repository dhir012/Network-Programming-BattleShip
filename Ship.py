from server import BOARD_SIZE

class Ship:
    def __init__(self, size, coordinates):
        self.size = size  # Size of the ship (e.g., 2 for a 2-cell ship)
        self.coordinates = coordinates  # List of coordinates for the ship's cells

    def is_sunk(self, hits):
        # Return True if all coordinates of the ship have been hit
        return all(coord in hits for coord in self.coordinates)

def place_ship(board, size, start_pos, orientation):
    # Simple function to place a ship on the board. Returns the list of coordinates for the ship.
    x, y = start_pos
    coordinates = []

    if orientation == "horizontal":
        for i in range(size):
            coordinates.append((x + i, y))
    elif orientation == "vertical":
        for i in range(size):
            coordinates.append((x, y + i))

    # Place the ship on the board by marking the coordinates
    for coord in coordinates:
        if coord[0] < 0 or coord[0] >= BOARD_SIZE or coord[1] < 0 or coord[1] >= BOARD_SIZE:
            raise ValueError("Ship is out of bounds!")
        if board[coord[1]][coord[0]] != 0:  # Check if the cell is already occupied
            raise ValueError("Cell already occupied!")
        board[coord[1]][coord[0]] = 1  # Mark the ship on the board

    return Ship(size, coordinates)
