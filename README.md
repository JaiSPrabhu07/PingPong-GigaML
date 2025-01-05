

```markdown
# Ping Pong Game 

This project implements a simple Pong game using FastAPI and WebSockets. The game features two players, a ball that moves automatically, paddle control via WebSocket, and obstacles. The game is continuously updated in the background and broadcasts the state to all connected clients.

## Features

- Real-time two-player Pong game.
- Ball movement and collision detection with paddles, walls, and obstacles.
- Scoring system for both players.
- Obstacles that interact with the ball.
- WebSocket communication to send paddle positions and game updates.
- Ball and game state are updated continuously in the background.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- `asyncio` (for background tasks)
- `random` (for generating obstacles)

## Setup

### 1. Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/JaiSPrabhu07/PingPong-GigaML
cd PingPong-GigaML
```

### 2. Install dependencies

Install the necessary Python dependencies:

```bash
pip install fastapi uvicorn
```

### 3. Run the server

Run the FastAPI application with `uvicorn`. This will start the server on `http://127.0.0.1:8000`:

```bash
uvicorn main:app --reload
```

This will start the FastAPI application, which listens for WebSocket connections on `/ws/{player_id}`.

### 4. Connect to the game via WebSocket

You can connect to the game using a WebSocket client. Replace `{player_id}` with either `player1` or `player2` to connect each player:

```bash
ws://127.0.0.1:8000/ws/player1
```

or

```bash
ws://127.0.0.1:8000/ws/player2
```

### 5. Game Controls

- The paddle positions are updated by sending a JSON message from the client.
- The paddle object in the message should look like this:
  ```json
  {
    "paddle": {
      "x": <paddle_x_position>,
      "y": <paddle_y_position>
    }
  }
  ```

  Example WebSocket message to update `player1` paddle:
  ```json
  {
    "paddle": {
      "x": 10,
      "y": 150
    }
  }
  ```

### 6. Game State

The game state is continuously updated and broadcast to all connected clients. The state includes:
- Ball position (`ball.x`, `ball.y`)
- Ball velocity (`ball.dx`, `ball.dy`)
- Player scores (`scores.player1`, `scores.player2`)
- Obstacle positions (`obstacles`)

The game state is sent to all clients every time it is updated, ensuring all players see the same view of the game.

### 7. Background Task

The ball moves automatically and updates in the background. This task runs continuously, with the ball being updated every 16 milliseconds (about 60 FPS). The background task is started when the server starts.

### 8. Score System

- Player 1 scores a point when the ball crosses the left side of the screen.
- Player 2 scores a point when the ball crosses the right side of the screen.
- The game state includes the updated scores for each player.

### 9. Obstacles

The game includes randomly placed obstacles that interact with the ball. When the ball collides with an obstacle, it changes direction.

## Example WebSocket Client (Optional)

If you prefer not to use a WebSocket client directly, you can test the game with a simple WebSocket client in Python using `websockets` library.

First, install the `websockets` library:

```bash
pip install websockets
```

Then, create a simple WebSocket client to simulate paddle movement:

```python
import websockets
import asyncio
import json

async def move_paddle():
    uri = "ws://127.0.0.1:8000/ws/player1"  # or ws://127.0.0.1:8000/ws/player2 for player 2
    async with websockets.connect(uri) as websocket:
        while True:
            # Send paddle movement
            paddle_position = {"x": 10, "y": 150}  # Example position for player1
            await websocket.send(json.dumps({"paddle": paddle_position}))

            # Wait for a short time before sending the next position
            await asyncio.sleep(0.016)  # ~60 FPS

asyncio.run(move_paddle())
```

## Project Structure

```
websocket-pong-game/
│
├── main.py         # FastAPI server and WebSocket game logic
└── README.md       # This file
```

