from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
socketio = SocketIO(app)

games = {}  # Dictionary to store game state

@app.route('/')
def index():
    return render_template('index.html')  # Frontend webpage

@socketio.on('join_game')
def handle_join(data):
    player = data['player']
    game_id = data['game_id']

    if game_id not in games:
        games[game_id] = {'players': [], 'board': [[" "] * 10 for _ in range(10)]}

    if len(games[game_id]['players']) < 2:
        games[game_id]['players'].append(player)
        join_room(game_id)
        emit('player_joined', {'message': f'{player} has joined the game!'}, room=game_id)

    if len(games[game_id]['players']) == 2:
        emit('start_game', {'message': 'Game is starting!'}, room=game_id)

@socketio.on('move')
def handle_move(data):
    game_id = data['game_id']
    x, y = data['coordinates']

    # Logic for handling moves
    board = games[game_id]['board']
    result = 'Hit' if board[x][y] == 'ship' else 'Miss'
    board[x][y] = 'X' if result == 'Hit' else 'O'

    emit('move_result', {'result': result, 'coordinates': (x, y)}, room=game_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)