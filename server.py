from flask import Flask, render_template, request  # Added request
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []
lock = threading.Lock()

# Game state variables
game_state = {
    'player_ready': [False, False],
    'turn': 0,
    'grids': [{}, {}],  # Ship positions for both players
    'hits': [0, 0],     # Hits for each player
    'total_ship_cells': 17
}

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    global clients
    with lock:
        if len(clients) < 2:
            clients.append(request.sid)
            player_id = len(clients) - 1
            emit('assign_player_id', {'player_id': player_id})
            print(f"Player {player_id} connected.")
        else:
            emit('connection_refused', {'message': 'Server full'})
            return


@socketio.on('place_ships')
def place_ships(data):
    global game_state
    player_id = data['player_id']
    with lock:
        game_state['grids'][player_id] = data['grid']
        game_state['player_ready'][player_id] = True
        print(f"Player {player_id} placed their ships.")
        emit('update_status', {'message': 'Waiting for opponent...'})
        if all(game_state['player_ready']):
            socketio.emit('start_game', {'message': 'Game is starting! Player 0 begins.'})


@socketio.on('make_move')
def make_move(data):
    global game_state
    player_id = data['player_id']
    if player_id != game_state['turn']:
        emit('invalid_move', {'message': 'Not your turn!'})
        return

    opponent_id = 1 - player_id
    x, y = data['x'], data['y']
    opponent_grid = game_state['grids'][opponent_id]

    # Check hit or miss
    result = 'MISS'
    if (x, y) in opponent_grid and opponent_grid[(x, y)] == 'SHIP':
        result = 'HIT'
        game_state['hits'][player_id] += 1

    emit('move_result', {'x': x, 'y': y, 'result': result, 'player_id': player_id}, broadcast=True)

    # Check for win
    if game_state['hits'][player_id] == game_state['total_ship_cells']:
        socketio.emit('game_over', {'winner': player_id})
        return

    # Update turn
    game_state['turn'] = opponent_id
    socketio.emit('update_turn', {'turn': game_state['turn']})


@socketio.on('disconnect')
def on_disconnect():
    global clients
    with lock:
        clients = []
        socketio.emit('game_reset', {'message'})
