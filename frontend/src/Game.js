import React, { useState, useEffect, useRef } from "react";
import "./Game.css";

const Game = ({ player }) => {
    const [gameState, setGameState] = useState({
        ball: { x: 300, y: 200 },
        player1_paddle: { y: 150 },
        player2_paddle: { y: 150 },
        obstacles: [],
        score: { player1: 0, player2: 0 },
    });

    const socketRef = useRef(null);

    useEffect(() => {
        socketRef.current = new WebSocket("ws://localhost:8000/ws");

        socketRef.current.onopen = () => {
            console.log("WebSocket connected");
        };

        socketRef.current.onmessage = (event) => {
            const updatedGameState = JSON.parse(event.data);
            setGameState(updatedGameState);
        };

        socketRef.current.onclose = () => {
            console.log("WebSocket disconnected");
        };

        return () => socketRef.current.close();
    }, []);

    const handleKeyDown = (e) => {
        let direction = null;

        if (e.key === "w" || e.key === "ArrowUp") direction = "up";
        if (e.key === "s" || e.key === "ArrowDown") direction = "down";

        if (direction) {
            socketRef.current.send(
                JSON.stringify({ player, direction })
            );
        }
    };

    useEffect(() => {
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, []);

    return (
        <div className="game-container">
            <div className="scoreboard">
                <span>Player 1: {gameState.score?.player1 ?? 0}</span>
                <span>Player 2: {gameState.score?.player2 ?? 0}</span>
            </div>
            <div className="game-area">
                <div
                    className="ball"
                    style={{
                        left: `${gameState.ball.x}px`,
                        top: `${gameState.ball.y}px`,
                    }}
                ></div>
                <div
                    className="paddle player1-paddle"
                    style={{ top: `${gameState.player1_paddle.y}px` }}
                ></div>
                <div
                    className="paddle player2-paddle"
                    style={{ top: `${gameState.player2_paddle.y}px` }}
                ></div>
                {gameState.obstacles.map((obs, idx) => (
                    <div
                        key={idx}
                        className="obstacle"
                        style={{
                            left: `${obs.x}px`,
                            top: `${obs.y}px`,
                        }}
                    ></div>
                ))}
            </div>
        </div>
    );
};

export default Game;
