from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
socketio = SocketIO(app)

# Game state
games = {}
waiting_players = []  # A list to keep track of players waiting for an opponent


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('find_player')
def handle_find_player(data):
    player_name = data['name']
    player_id = random.randint(1, 10000)  # Random player ID

    # Add player to waiting list
    waiting_players.append(player_id)

    # Check if there's another player waiting
    if len(waiting_players) >= 2:
        # Match players
        player1_id = waiting_players.pop(0)  # First player
        player2_id = waiting_players.pop(0)  # Second player

        games[player1_id] = {
            'player_name': player_name,
            'opponent_name': None,
            'player_ships': [],
            'opponent_ships': [],
            'is_player_turn': True,
            'game_started': False
        }
        games[player2_id] = {
            'player_name': 'Opponent',
            'opponent_name': player_name,
            'player_ships': [],
            'opponent_ships': [],
            'is_player_turn': False,
            'game_started': False
        }
        # Notify both players to start the game
        emit('start_game', {'player_id': player1_id}, room=player1_id)
        emit('start_game', {'player_id': player2_id}, room=player2_id)

    else:
        # If no opponent is found yet, let the player know they are waiting
        emit('waiting_for_opponent', {'message': 'Waiting for an opponent...'}, room=player_id)


@socketio.on('start_game')
def start_game(data):
    player_id = data['player_id']
    if games.get(player_id):
        games[player_id]['game_started'] = True
        games[player_id]['is_player_turn'] = True  # First player starts the game
        emit('game_started', {'message': 'Game has started! It\'s your turn.'}, room=player_id)


# Example of handling moves
@socketio.on('move')
def handle_move(data):
    player_id = data['player_id']
    opponent_id = games[player_id]['opponent_id']
    x, y = data['x'], data['y']

    # Example move logic (hit or miss):
    if games[opponent_id]['player_ships'][y][x] == 'ship':
        emit('move_result', {'x': x, 'y': y, 'result': 'Hit'}, room=player_id)
        # Check if all ships are hit and declare winner
        # (You can add logic for checking if the game is over)
    else:
        emit('move_result', {'x': x, 'y': y, 'result': 'Miss'}, room=player_id)


if __name__ == '__main__':
    socketio.run(app)
