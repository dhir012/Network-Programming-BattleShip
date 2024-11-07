#Function checks whether a cell on the board is occupied by a ship
def attack(board, x, y):
    if board[y][x] == 1:
        board[y][x] = 2  # Mark the cell as hit
        return True  # Successful hit
    else:
        board[y][x] = 3  # Mark the cell as missed
        return False  # Missed attacked