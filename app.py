from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Game state variables
players = []  # List to hold player connections
player_ready = [False, False]  # Track if players have placed their ships
total_ship_cells = 17  # Number of ship cells each player has
player_hits = [0, 0]  # Number of hits each player has made

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global players
    if len(players) < 2:
        players.append(request.sid)
        player_id = len(players) - 1
        emit('PLAYER_ID', player_id)
        print(f"Player {player_id} connected: {request.sid}")
    else:
        emit('GAME_FULL')

@socketio.on('disconnect')
def handle_disconnect():
    global players
    print(f"Client disconnected: {request.sid}")
    if request.sid in players:
        players.remove(request.sid)
        emit('PLAYER_DISCONNECTED', broadcast=True)

@socketio.on('PLACEMENT_DONE')
def handle_placement_done(player_id):
    global player_ready
    player_ready[player_id] = True
    if all(player_ready):
        emit('START_GAME', broadcast=True)

@socketio.on('MOVE')
def handle_move(data):
    global player_hits
    x = data['x']
    y = data['y']
    result = data['result']
    player_id = data['player_id']

    emit('RESULT', {'x': x, 'y': y, 'result': result, 'player_id': player_id}, broadcast=True)

    if result == 'HIT':
        player_hits[player_id] += 1
        if player_hits[player_id] == total_ship_cells:
            emit('WINNER', f'Player {player_id}', broadcast=True)
            reset_game()

def reset_game():
    global player_ready, player_hits
    player_ready = [False, False]
    player_hits = [0, 0]

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

