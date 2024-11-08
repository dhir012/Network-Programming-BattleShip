import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
clients = []
lock = threading.Lock()
player_ready = [False, False]
game_started = False
player_hits = [0, 0]
total_ship_cells = 17  # ship cells for each player

def handle_client(conn, addr, player_id):
    # handles client connections and game data
    global clients, game_started, player_ready, player_hits

    conn.sendall(f"PLAYER_ID:{player_id}".encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            with lock:
                if data == "PLACEMENT_DONE":
                    player_ready[player_id] = True
                    if all(player_ready):
                        game_started = True
                        broadcast("START_GAME")

                elif data.startswith("MOVE:"):
                    x, y, result = data.split(":")[1].split(",")
                    x, y = int(x), int(y)
                    broadcast(f"RESULT:{x},{y},{result}")

                    if result == "HIT":
                        player_hits[player_id] += 1
                        if player_hits[player_id] == total_ship_cells:
                            broadcast(f"WINNER:Player {player_id}")
                            break
        except:
            break

    with lock:
        clients.remove(conn)
    conn.close()

def broadcast(message):
    # sends message to all clients connected
    for client in clients:
        client.sendall(message.encode())

def main():
    # accept and manage client connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Server listening on {HOST}:{PORT}")

    player_id = 0
    while len(clients) < 2:
        conn, addr = server.accept()
        with lock:
            clients.append(conn)
        print(f"Connected by {addr}")
        threading.Thread(target=handle_client, args=(conn, addr, player_id)).start()
        player_id += 1

if __name__ == "__main__":
    main()
