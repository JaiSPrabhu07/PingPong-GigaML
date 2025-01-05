from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

game_state = {
    "ball": {"x": 300, "y": 200, "dx": 3, "dy": 3},
    "player1_paddle": {"y": 150},
    "player2_paddle": {"y": 150},
    "obstacles": [{"x": 200, "y": 100}, {"x": 400, "y": 300}],
    "score": {"player1": 0, "player2": 0},
}

async def game_loop():
    while True:
        # Update ball position
        game_state["ball"]["x"] += game_state["ball"]["dx"]
        game_state["ball"]["y"] += game_state["ball"]["dy"]

        # Bounce off top and bottom walls
        if game_state["ball"]["y"] <= 0 or game_state["ball"]["y"] >= 380:
            game_state["ball"]["dy"] *= -1

        # Bounce off paddles
        if game_state["ball"]["x"] <= 10 and game_state["player1_paddle"]["y"] <= game_state["ball"]["y"] <= game_state["player1_paddle"]["y"] + 80:
            game_state["ball"]["dx"] *= -1
        elif game_state["ball"]["x"] >= 580 and game_state["player2_paddle"]["y"] <= game_state["ball"]["y"] <= game_state["player2_paddle"]["y"] + 80:
            game_state["ball"]["dx"] *= -1

        # Check for scoring
        if game_state["ball"]["x"] < 0:
            game_state["score"]["player2"] += 1
            reset_ball()
        elif game_state["ball"]["x"] > 600:
            game_state["score"]["player1"] += 1
            reset_ball()

        # Broadcast game state
        await manager.broadcast(game_state)
        await asyncio.sleep(0.016)

def reset_ball():
    game_state["ball"] = {"x": 300, "y": 200, "dx": 3, "dy": 3}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            player = data.get("player")
            direction = data.get("direction")

            if player == "player1":
                move_paddle("player1_paddle", direction)
            elif player == "player2":
                move_paddle("player2_paddle", direction)

            await manager.broadcast(game_state)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def move_paddle(paddle, direction):
    if direction == "up":
        game_state[paddle]["y"] = max(0, game_state[paddle]["y"] - 10)
    elif direction == "down":
        game_state[paddle]["y"] = min(320, game_state[paddle]["y"] + 10)

# Start game loop
@app.on_event("startup")
async def start_game_loop():
    asyncio.create_task(game_loop())
