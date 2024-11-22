  document.addEventListener('DOMContentLoaded', () => {
    const playerGrid = document.querySelector('.grid-user')
    const enemyGrid = document.querySelector('.grid-computer')
    const userDisplayGrid = document.querySelector('.grid-display')
    const allShips = document.querySelectorAll('.ship')
    const destroyerShip = document.querySelector('.destroyer-container')
    const submarineShip = document.querySelector('.submarine-container')
    const cruiserShip = document.querySelector('.cruiser-container')
    const battleshipShip = document.querySelector('.battleship-container')
    const carrierShip = document.querySelector('.carrier-container')
    const startGameButton = document.querySelector('#start')
    const rotateShipButton = document.querySelector('#rotate')
    const turnIndicator = document.querySelector('#whose-go')
    const gameInfoDisplay = document.querySelector('#info')
    const buttonSetup = document.getElementById('setup-buttons')
    const playerSquares = []
    const enemySquares = []
    let horizontalOrientation = true
    let gameFinished = false
    let activePlayer = 'user'
    const gridWidth = 10
    let playerNumber = 0
    let isPlayerReady = false
    let isEnemyReady = false
    let allShipsPlaced = false
    let lastFiredShot = -1

      // ships
    const shipArray = [
      {
        name: 'destroyer',
        directions: [
          [0, 1],
          [0, gridWidth]
        ]
      },
      {
        name: 'submarine',
        directions: [
          [0, 1, 2],
          [0, gridWidth, gridWidth*2]
        ]
      },
      {
        name: 'cruiser',
        directions: [
          [0, 1, 2],
          [0, gridWidth, gridWidth*2]
        ]
      },
      {
        name: 'battleship',
        directions: [
          [0, 1, 2, 3],
          [0, gridWidth, gridWidth*2, gridWidth*3]
        ]
      },
      {
        name: 'carrier',
        directions: [
          [0, 1, 2, 3, 4],
          [0, gridWidth, gridWidth*2, gridWidth*3, gridWidth*4]
        ]
      },
    ]

    makeBoard(playerGrid, playerSquares)
    makeBoard(enemyGrid, enemySquares)

    // player mode - no single player just here because original code breaks without it
    if (gameMode === 'singlePlayer') {
      startSinglePlayer()
    } else {
      startMultiPlayer()
    }

    // multiplayer
    function startMultiPlayer() {
      const socket = io();

      // player number
      socket.on('player-number', num => {
        if (num === -1) {
          gameInfoDisplay.innerHTML = "Sorry, the server is full"
        } else {
          playerNumber = parseInt(num)
          if(playerNumber === 1) activePlayer = "enemy"

          console.log(playerNumber)

          // player status
          socket.emit('check-players')
        }
      })

      // player has connected / disconnected
      socket.on('player-connection', num => {
        console.log(`Player number ${num} has connected or disconnected`)
        playerCurrentConnection(num)
      })

      // enemy ready
      socket.on('enemy-ready', num => {
        isEnemyReady = true
        playerReady(num)
        if (isPlayerReady) {
          playGameMulti(socket)
          buttonSetup.style.display = 'none'
        }
      })

      // player status
      socket.on('check-players', players => {
        players.forEach((p, i) => {
          if(p.connected) playerCurrentConnection(i)
          if(p.ready) {
            playerReady(i)
            if(i !== playerReady) isEnemyReady = true
          }
        })
      })

      // timeout
      socket.on('timeout', () => {
        gameInfoDisplay.innerHTML = 'You have reached the 5 minute limit'
      })

      // ready button
      startGameButton.addEventListener('click', () => {
        if(allShipsPlaced) playGameMulti(socket)
        else gameInfoDisplay.innerHTML = "Please place all ships"
      })

      // firing
      enemySquares.forEach(square => {
        square.addEventListener('click', () => {
          if(activePlayer === 'user' && isPlayerReady && isEnemyReady) {
            lastFiredShot = square.dataset.id
            socket.emit('fire', lastFiredShot)
          }
        })
      })

      // fire received
      socket.on('fire', id => {
        enemyTurn(id)
        const square = playerSquares[id]
        socket.emit('fire-reply', square.classList)
        playGameMulti(socket)
      })

      // fire reply
      socket.on('fire-reply', classList => {
        revealSquare(classList)
        playGameMulti(socket)
      })

      function playerCurrentConnection(num) {
        let player = `.p${parseInt(num) + 1}`
        document.querySelector(`${player} .connected`).classList.toggle('active')
        if(parseInt(num) === playerNumber) document.querySelector(player).style.fontWeight = 'bold'
      }
    }

    // make board
    function makeBoard(grid, squares) {
      for (let i = 0; i < gridWidth*gridWidth; i++) {
        const square = document.createElement('div')
        square.dataset.id = i
        grid.appendChild(square)
        squares.push(square)
      }
    }

    // place ships in random locations
    function generate(ship) {
      let randomDirection = Math.floor(Math.random() * ship.directions.length)
      let current = ship.directions[randomDirection]
      if (randomDirection === 0) direction = 1
      if (randomDirection === 1) direction = 10
      let randomStart = Math.abs(Math.floor(Math.random() * enemySquares.length - (ship.directions[0].length * direction)))

      const isTaken = current.some(index => enemySquares[randomStart + index].classList.contains('taken'))
      const isAtRightEdge = current.some(index => (randomStart + index) % gridWidth === gridWidth - 1)
      const isAtLeftEdge = current.some(index => (randomStart + index) % gridWidth === 0)

      if (!isTaken && !isAtRightEdge && !isAtLeftEdge) current.forEach(index => enemySquares[randomStart + index].classList.add('taken', ship.name))

      else generate(ship)
    }


    // rotate ships
    function rotate() {
      if (horizontalOrientation) {
        destroyerShip.classList.toggle('destroyer-container-vertical')
        submarineShip.classList.toggle('submarine-container-vertical')
        cruiserShip.classList.toggle('cruiser-container-vertical')
        battleshipShip.classList.toggle('battleship-container-vertical')
        carrierShip.classList.toggle('carrier-container-vertical')
        horizontalOrientation = false
        return
      }
      if (!horizontalOrientation) {
        destroyerShip.classList.toggle('destroyer-container-vertical')
        submarineShip.classList.toggle('submarine-container-vertical')
        cruiserShip.classList.toggle('cruiser-container-vertical')
        battleshipShip.classList.toggle('battleship-container-vertical')
        carrierShip.classList.toggle('carrier-container-vertical')
        horizontalOrientation = true
        return
      }
    }
    rotateShipButton.addEventListener('click', rotate)

    // move each ship
    allShips.forEach(ship => ship.addEventListener('dragstart', dragStart))
    playerSquares.forEach(square => square.addEventListener('dragstart', dragStart))
    playerSquares.forEach(square => square.addEventListener('dragover', dragOver))
    playerSquares.forEach(square => square.addEventListener('dragenter', dragEnter))
    playerSquares.forEach(square => square.addEventListener('dragleave', dragLeave))
    playerSquares.forEach(square => square.addEventListener('drop', dragDrop))
    playerSquares.forEach(square => square.addEventListener('dragend', dragEnd))

    let selectedShipNameWithIndex
    let draggedShip
    let draggedShipLength

    allShips.forEach(ship => ship.addEventListener('mousedown', (e) => {
      selectedShipNameWithIndex = e.target.id
    }))

    function dragStart() {
      draggedShip = this
      draggedShipLength = this.childNodes.length
    }

    function dragOver(e) {
      e.preventDefault()
    }

    function dragEnter(e) {
      e.preventDefault()
    }

    function dragLeave() {
    }

    function dragDrop() {
      let shipNameWithLastId = draggedShip.lastChild.id
      let shipClass = shipNameWithLastId.slice(0, -2)
      let lastShipIndex = parseInt(shipNameWithLastId.substr(-1))
      let shipLastId = lastShipIndex + parseInt(this.dataset.id)
      const notAllowedHorizontal = [0,10,20,30,40,50,60,70,80,90,1,11,21,31,41,51,61,71,81,91,2,22,32,42,52,62,72,82,92,3,13,23,33,43,53,63,73,83,93]
      const notAllowedVertical = [99,98,97,96,95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60]

      let newNotAllowedHorizontal = notAllowedHorizontal.splice(0, 10 * lastShipIndex)
      let newNotAllowedVertical = notAllowedVertical.splice(0, 10 * lastShipIndex)

      selectedShipIndex = parseInt(selectedShipNameWithIndex.substr(-1))

      shipLastId = shipLastId - selectedShipIndex

      if (horizontalOrientation && !newNotAllowedHorizontal.includes(shipLastId)) {
        for (let i=0; i < draggedShipLength; i++) {
          let directionClass
          if (i === 0) directionClass = 'start'
          if (i === draggedShipLength - 1) directionClass = 'end'
          playerSquares[parseInt(this.dataset.id) - selectedShipIndex + i].classList.add('taken', 'horizontal', directionClass, shipClass)
        }
      } else if (!horizontalOrientation && !newNotAllowedVertical.includes(shipLastId)) {
        for (let i=0; i < draggedShipLength; i++) {
          let directionClass
          if (i === 0) directionClass = 'start'
          if (i === draggedShipLength - 1) directionClass = 'end'
          playerSquares[parseInt(this.dataset.id) - selectedShipIndex + gridWidth*i].classList.add('taken', 'vertical', directionClass, shipClass)
        }
      } else return

      userDisplayGrid.removeChild(draggedShip)
      if(!userDisplayGrid.querySelector('.ship')) allShipsPlaced = true
    }

    function dragEnd() {
    }

    // game logic
    function playGameMulti(socket) {
      buttonSetup.style.display = 'none'
      if(gameFinished) return
      if(!isPlayerReady) {
        socket.emit('player-ready')
        isPlayerReady = true
        playerReady(playerNumber)
      }

      if(isEnemyReady) {
        if(activePlayer === 'user') {
          turnIndicator.innerHTML = 'Your Go'
        }
        if(activePlayer === 'enemy') {
          turnIndicator.innerHTML = "Enemy's Go"
        }
      }
    }

    function playerReady(num) {
      let player = `.p${parseInt(num) + 1}`
      document.querySelector(`${player} .ready`).classList.toggle('active')
    }

    // code not used within program
    function oldSingleGame() {
      if (gameFinished) return
      if (activePlayer === 'user') {
        turnIndicator.innerHTML = 'Your Go'
        enemySquares.forEach(square => square.addEventListener('click', function(e) {
          lastFiredShot = square.dataset.id
          revealSquare(square.classList)
        }))
      }
      if (activePlayer === 'enemy') {
        turnIndicator.innerHTML = 'Computers Go'
        setTimeout(enemyTurn, 1000)
      }
    }

    let destroyerCount = 0
    let submarineCount = 0
    let cruiserCount = 0
    let battleshipCount = 0
    let carrierCount = 0

    function revealSquare(classList) {
      const enemySquare = enemyGrid.querySelector(`div[data-id='${lastFiredShot}']`)
      const obj = Object.values(classList)
      if (!enemySquare.classList.contains('boom') && activePlayer === 'user' && !gameFinished) {
        if (obj.includes('destroyer')) destroyerCount++
        if (obj.includes('submarine')) submarineCount++
        if (obj.includes('cruiser')) cruiserCount++
        if (obj.includes('battleship')) battleshipCount++
        if (obj.includes('carrier')) carrierCount++
      }
      if (obj.includes('taken')) {
        enemySquare.classList.add('boom')
      } else {
        enemySquare.classList.add('miss')
      }
      checkingForWin()
      activePlayer = 'enemy'
      if(gameMode === 'singlePlayer') oldSingleGame()
    }

    let cpuDestroyerHits = 0
    let cpuSubmarineHits = 0
    let cpuCruiserHits = 0
    let cpuBattleshipHits = 0
    let cpuCarrierHits = 0


    function enemyTurn(square) {
      if (gameMode === 'singlePlayer') square = Math.floor(Math.random() * playerSquares.length)
      if (!playerSquares[square].classList.contains('boom')) {
        const hit = playerSquares[square].classList.contains('taken')
        playerSquares[square].classList.add(hit ? 'boom' : 'miss')
        if (playerSquares[square].classList.contains('destroyer')) cpuDestroyerHits++
        if (playerSquares[square].classList.contains('submarine')) cpuSubmarineHits++
        if (playerSquares[square].classList.contains('cruiser')) cpuCruiserHits++
        if (playerSquares[square].classList.contains('battleship')) cpuBattleshipHits++
        if (playerSquares[square].classList.contains('carrier')) cpuCarrierHits++
        checkingForWin()
      } else if (gameMode === 'singlePlayer') enemyTurn()
      activePlayer = 'user'
      turnIndicator.innerHTML = 'Your Go'
    }

    function checkingForWin() {
      let enemy = 'computer'
      if(gameMode === 'multiPlayer') enemy = 'enemy'
      if (destroyerCount === 2) {
        gameInfoDisplay.innerHTML = `You sunk the ${enemy}'s destroyer`
        destroyerCount = 10
      }
      if (submarineCount === 3) {
        gameInfoDisplay.innerHTML = `You sunk the ${enemy}'s submarine`
        submarineCount = 10
      }
      if (cruiserCount === 3) {
        gameInfoDisplay.innerHTML = `You sunk the ${enemy}'s cruiser`
        cruiserCount = 10
      }
      if (battleshipCount === 4) {
        gameInfoDisplay.innerHTML = `You sunk the ${enemy}'s battleship`
        battleshipCount = 10
      }
      if (carrierCount === 5) {
        gameInfoDisplay.innerHTML = `You sunk the ${enemy}'s carrier`
        carrierCount = 10
      }
      if (cpuDestroyerHits === 2) {
        gameInfoDisplay.innerHTML = `${enemy} sunk your destroyer`
        cpuDestroyerHits = 10
      }
      if (cpuSubmarineHits === 3) {
        gameInfoDisplay.innerHTML = `${enemy} sunk your submarine`
        cpuSubmarineHits = 10
      }
      if (cpuCruiserHits === 3) {
        gameInfoDisplay.innerHTML = `${enemy} sunk your cruiser`
        cpuCruiserHits = 10
      }
      if (cpuBattleshipHits === 4) {
        gameInfoDisplay.innerHTML = `${enemy} sunk your battleship`
        cpuBattleshipHits = 10
      }
      if (cpuCarrierHits === 5) {
        gameInfoDisplay.innerHTML = `${enemy} sunk your carrier`
        cpuCarrierHits = 10
      }

      if ((destroyerCount + submarineCount + cruiserCount + battleshipCount + carrierCount) === 50) {
        gameInfoDisplay.innerHTML = "YOU WIN"
        gameDone()
      }
      if ((cpuDestroyerHits + cpuSubmarineHits + cpuCruiserHits + cpuBattleshipHits + cpuCarrierHits) === 50) {
        gameInfoDisplay.innerHTML = `${enemy.toUpperCase()} WINS`
        gameDone()
      }
    }

    function gameDone() {
      gameFinished = true
      startGameButton.removeEventListener('click', oldSingleGame)
    }
  })
