#Manage overall game flow
import pygame
import pygame.gfxdraw

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.winner = None

    def start_game(self):
        while not self.winner:
            self.play_turn()
            self.check_winner()
        print(f"Game Over! {self.winner.name} wins!")

    def play_turn(self):
        print(f"{self.current_player.name}'s turn")
        self.current_player.attack(self.opponent())

        # Alternate turns
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def check_winner(self):
        if self.player1.remaining_ships == 0:
            self.winner = self.player2
        elif self.player2.remaining_ships == 0:
            self.winner = self.player1

    def opponent(self):
        return self.player2 if self.current_player == self.player1 else self.player1
if __name__ == "__main__":
    main()