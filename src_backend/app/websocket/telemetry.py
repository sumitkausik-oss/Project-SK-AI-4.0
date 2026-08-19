"""
SK Enterprises | WebSocket Real-Time Telemetry Manager
Inventor & Sole Architect: Sumeet Kumar
"""
import time
import asyncio
from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from src_backend.app.core.logging_config import get_logger
from src_backend.app.services.agent_town_service import AGENTS_STATE

logger = get_logger(__name__)

class TelemetryConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total active: {len(self.active_connections)}")

    async def broadcast_telemetry(self):
        """Continuously streams real-time telemetry metrics to connected frontends."""
        while True:
            if self.active_connections:
                payload = {
                    "fps": 60,
                    "timestamp": time.time(),
                    "neural_coherence": 100.0,
                    "active_agents": len(AGENTS_STATE),
                    "agents": AGENTS_STATE
                }
                for connection in list(self.active_connections):
                    try:
                        await connection.send_json(payload)
                    except Exception:
                        self.disconnect(connection)
            await asyncio.sleep(0.5)

telemetry_manager = TelemetryConnectionManager()

async def websocket_telemetry_endpoint(websocket: WebSocket):
    await telemetry_manager.connect(websocket)
    try:
        while True:
            # Keep socket open and process any incoming client pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        telemetry_manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket unexpected exit: {e}")
        telemetry_manager.disconnect(websocket)
