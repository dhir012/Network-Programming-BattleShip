const express = require('express')
const path = require('path')
const http = require('http')
const PORT = process.env.PORT || 3002
const socketio = require('socket.io')
const app = express()
const server = http.createServer(app)
const io = socketio(server)

// static folder
app.use(express.static(path.join(__dirname, "public")))

// start server
server.listen(PORT, () => console.log(`Server running on port ${PORT}`))
const connections = [null, null]

io.on('connection', socket => {

  // find an available player number
  let playerIndex = -1;
  for (const i in connections) {
    if (connections[i] === null) {
      playerIndex = i
      break
    }
  }
  socket.emit('player-number', playerIndex)

  console.log(`Player ${playerIndex} has connected`)

  // ignore player 3
  if (playerIndex === -1) return

  connections[playerIndex] = false

  // what player just connected
  socket.broadcast.emit('player-connection', playerIndex)

  // handle disconnect
  socket.on('disconnect', () => {
    console.log(`Player ${playerIndex} disconnected`)
    connections[playerIndex] = null
    socket.broadcast.emit('player-connection', playerIndex)
  })

  // ready
  socket.on('player-ready', () => {
    socket.broadcast.emit('enemy-ready', playerIndex)
    connections[playerIndex] = true
  })

  // check connections
  socket.on('check-players', () => {
    const players = []
    for (const i in connections) {
      connections[i] === null ? players.push({connected: false, ready: false}) : players.push({connected: true, ready: connections[i]})
    }
    socket.emit('check-players', players)
  })

  // fire received
  socket.on('fire', id => {
    console.log(`Shot fired from ${playerIndex}`, id)
    socket.broadcast.emit('fire', id)
  })

  // fire reply
  socket.on('fire-reply', square => {
    console.log(square)

    // forward reply to other player
    socket.broadcast.emit('fire-reply', square)
  })

  // timeout connection
  setTimeout(() => {
    connections[playerIndex] = null
    socket.emit('timeout')
    socket.disconnect()
  }, 300000) // 5 minute timeout
})