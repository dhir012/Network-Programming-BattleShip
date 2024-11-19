const socket = io();
let playerId;
let isMyTurn = false;
let shipPlacementPhase = true;

const playerGrid = document.getElementById("player-grid");
const opponentGrid = document.getElementById("opponent-grid");

function createGrid(gridElement, isOpponent = false) {
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 10; j++) {
            const cell = document.createElement("div");
            cell.dataset.row = i;
            cell.dataset.col = j;

            if (!isOpponent) {
                cell.addEventListener("click", () => placeShip(cell));
            } else {
                cell.addEventListener("click", () => makeMove(cell));
            }

            gridElement.appendChild(cell);
        }
    }
}

function placeShip(cell) {
    if (!shipPlacementPhase) return;
    cell.classList.toggle("ship");
}

function makeMove(cell) {
    if (!isMyTurn || shipPlacementPhase) return;
    const x = cell.dataset.row;
    const y = cell.dataset.col;
    socket.emit("make_move", { player_id: playerId, x: parseInt(x), y: parseInt(y) });
}

document.getElementById("start-game").addEventListener("click", () => {
    const shipPositions = Array.from(playerGrid.children)
        .filter(cell => cell.classList.contains("ship"))
        .map(cell => [parseInt(cell.dataset.row), parseInt(cell.dataset.col)]);

    if (shipPositions.length < 17) {
        alert("Place all your ships before starting the game!");
        return;
    }

    const grid = {};
    shipPositions.forEach(([x, y]) => (grid[`${x},${y}`] = "SHIP"));
    socket.emit("place_ships", { player_id: playerId, grid });
});

socket.on("assign_player_id", data => {
    playerId = data.player_id;
    document.getElementById("game-status").textContent = `You are Player ${playerId}.`;
});

socket.on("start_game", () => {
    shipPlacementPhase = false;
    isMyTurn = playerId === 0;
    document.getElementById("start-game").disabled = true;
    document.getElementById("game-status").textContent = isMyTurn
        ? "Your turn!"
        : "Waiting for opponent's turn...";
});

socket.on("update_turn", data => {
    isMyTurn = data.turn === playerId;
    document.getElementById("game-status").textContent = isMyTurn
        ? "Your turn!"
        : "Waiting for opponent's turn...";
});

socket.on("move_result", data => {
    const { x, y, result, player_id } = data;
    const grid = player_id === playerId ? opponentGrid : playerGrid;
    const cell = grid.querySelector(`[data-row="${x}"][data-col="${y}"]`);
    cell.classList.add(result.toLowerCase());
});

socket.on("game_over", data => {
    const winner = data.winner;
    document.getElementById("game-status").textContent = `Player ${winner} wins!`;
});

createGrid(playerGrid);
createGrid(opponentGrid, true);
