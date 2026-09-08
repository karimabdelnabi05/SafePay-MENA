"""
SafePay MENA - Main Application Entry Point
FastAPI Gateway with REST Endpoints, WebSocket Real-Time Broadcasting, and Static UI Hosting.
"""

import os
import json
import asyncio
from typing import List, Optional
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.models import (
    TransactionRequest,
    RiskDecision,
    RiskTier,
    PresetScenario,
    BiometricStepUpRequest
)
from app.core.risk_engine import DeterministicRiskEngine
from app.services.telecom_gateway import telecom_gateway
from app.services.ai_agent import audit_agent
from app.services.audit_store import audit_store
from app.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Real-Time AI Telecom Fraud Shield for Instant Payments in MENA"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)
        for dead in dead_connections:
            self.disconnect(dead)

manager = ConnectionManager()

# Mount Static Files (Cyber Dashboard)
STATIC_DIR = Path(__file__).parent / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
async def serve_index():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "status": "SafePay MENA API Online",
        "docs": "/docs",
        "ws": "/ws/live-feed"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "active_websockets": len(manager.active_connections),
        "mode": "MOCK_DETERMINISTIC" if settings.USE_MOCK_TELECOM else "LIVE_CARRIER"
    }

@app.post("/api/v1/transfer/evaluate", response_model=RiskDecision)
async def evaluate_transaction(
    txn: TransactionRequest,
    scenario: Optional[PresetScenario] = Query(None, description="Optional preset scenario for hackathon demo")
):
    """
    Main Pre-Authorization Evaluation Hook.
    Executes in <200ms end-to-end:
    1. Telecom Gateway queries CAMARA APIs (<150ms).
    2. Deterministic Risk Engine calculates Risk Score & Decision (<10ms).
    3. Asynchronous AI Agent synthesizes regulatory compliance trace.
    4. Real-time telemetry broadcast to SOC dashboard via WebSockets.
    """
    # 1. Gather telecom signals
    signals = await telecom_gateway.evaluate_carrier_signals(
        raw_phone=txn.sender_phone,
        scenario_override=scenario
    )
    
    # 2. Deterministic risk calculation (<10ms)
    decision = DeterministicRiskEngine.evaluate(txn, signals)
    
    # 3. Asynchronous AI compliance trace generation
    trace = await audit_agent.generate_compliance_trace(txn, decision)
    decision.ai_compliance_trace = trace
    
    # 4. Broadcast live event to all connected dashboard clients
    event_payload = {
        "type": "TRANSACTION_EVALUATED",
        "transaction": txn.model_dump(mode="json"),
        "decision": decision.model_dump(mode="json")
    }
    asyncio.create_task(manager.broadcast(event_payload))
    asyncio.create_task(audit_store.persist_audit_record(txn, decision))
    
    return decision


@app.post("/api/v1/transfer/step-up/verify")
async def verify_step_up(payload: BiometricStepUpRequest):
    """
    Biometric Challenge Resolution.
    Receives Face ID confirmation from the user device and clears the payment.
    """
    if not payload.success:
        raise HTTPException(status_code=400, detail="Biometric authentication failed or cancelled by user.")
        
    resolution_event = {
        "type": "STEP_UP_RESOLVED",
        "transaction_id": payload.transaction_id,
        "status": "APPROVED_POST_BIOMETRIC",
        "message": f"Biometric {payload.biometric_type} verified successfully. Coercion challenge resolved. Payment released."
    }
    await manager.broadcast(resolution_event)
    return resolution_event

@app.websocket("/ws/live-feed")
async def websocket_live_feed(websocket: WebSocket):
    """Real-time telemetry and AI trace feed for the dashboard."""
    await manager.connect(websocket)
    try:
        # Send initial welcome and state
        await websocket.send_json({
            "type": "CONNECTION_ESTABLISHED",
            "message": "Connected to SafePay MENA Real-Time Security Operations Stream"
        })
        while True:
            # Keep connection open and listen for ping/heartbeats
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "PING":
                    await websocket.send_json({"type": "PONG"})
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# Serve remaining static assets (CSS, JS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    print("Starting SafePay MENA on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
