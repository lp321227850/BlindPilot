from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app import __version__
from app.agent.runner import AgentNotConfigured, AgentRunner
from app.config import settings
from app.devices.hub import DeviceHub
from app.devices.pairing import PairingStore
from app.safety.engine import SafetyEngine
from app.safety.redaction import redact_screen_state

safety = SafetyEngine()
hub = DeviceHub(safety)
pairing = PairingStore()
agent = AgentRunner(settings.agent_api_key)

app = FastAPI(title="BlindPilot", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.public_url],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


class PairComplete(BaseModel):
    pairing_code: str
    display_name: str = "phone"
    public_key: str | None = None


class ClassifyRequest(BaseModel):
    tool_name: str
    arguments: dict = Field(default_factory=dict)


class ScreenStateIn(BaseModel):
    package: str | None = None
    nodes: list[dict] = Field(default_factory=list)


@app.get("/health/live")
def live() -> dict:
    return {"ok": True, "service": "blindpilot", "version": __version__}


@app.get("/health/ready")
def ready() -> dict:
    return {
        "ok": True,
        "database": "deferred",
        "agent_configured": agent.available,
        "agent_status": "configured" if agent.available else "not_configured",
    }


@app.get("/v1/status")
def status() -> dict:
    return {
        "public_url": settings.public_url,
        "env": settings.env,
        "agent": "antigravity" if agent.available else "unconfigured",
        "devices": len(hub.tokens),
    }


@app.post("/v1/pair/start")
def pair_start() -> dict:
    item = pairing.start()
    return {"pairing_code": item.code, "expires_in": int(item.expires_at - time.time())}


@app.post("/v1/pair/complete")
def pair_complete(body: PairComplete) -> dict:
    record = pairing.complete(body.pairing_code, body.display_name, body.public_key)
    if record is None:
        raise HTTPException(status_code=400, detail="invalid or expired pairing code")
    hub.register(record["device_id"], record["device_token"])
    return record


@app.post("/v1/safety/classify")
def classify(body: ClassifyRequest) -> dict:
    decision = safety.classify(body.tool_name, body.arguments)
    return {
        "level": decision.level,
        "allowed": decision.allowed,
        "reason": decision.reason,
        "error_code": decision.error_code,
    }


@app.post("/v1/privacy/redact")
def redact(body: ScreenStateIn) -> dict:
    return redact_screen_state(body.model_dump())


@app.post("/v1/agent/observe-demo")
async def observe_demo() -> dict:
    try:
        return await agent.start_observe_task("打开设置")
    except AgentNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.websocket("/v1/device/ws")
async def device_ws(ws: WebSocket) -> None:
    await ws.accept()
    session = None
    try:
        hello = await ws.receive_json()
        if hello.get("type") != "hello":
            await ws.close(code=4400)
            return
        session = hub.authenticate(hello.get("device_id", ""), hello.get("device_token", ""))
        if session is None:
            await ws.send_json({"type": "error", "error_code": "UNAUTHENTICATED"})
            await ws.close(code=4401)
            return
        await ws.send_json(
            {
                "type": "hello_ok",
                "protocol_version": 1,
                "device_id": session.device_id,
                "generation": session.generation,
            }
        )
        while True:
            msg = await ws.receive_json()
            mtype = msg.get("type")
            if mtype == "ping":
                await ws.send_json({"type": "pong", "seq": msg.get("seq")})
                continue
            if mtype == "cancel_task":
                hub.cancel_task(session.device_id, msg.get("task_id", ""))
                await ws.send_json({"type": "cancel_ok", "task_id": msg.get("task_id")})
                continue
            if mtype == "command_result":
                await ws.send_json({"type": "ack", "command_id": msg.get("command_id")})
                continue
            if mtype == "local_stop":
                gen = hub.local_stop(session.device_id)
                await ws.send_json({"type": "stop_ok", "generation": gen})
                continue
            await ws.send_json({"type": "error", "error_code": "ACTION_NOT_SUPPORTED"})
    except WebSocketDisconnect:
        return


def issue_command(device_id: str, action: str, args: dict, task_id: str | None = None) -> dict:
    session = hub.sessions.get(device_id)
    if session is None:
        return {"ok": False, "error_code": "DEVICE_OFFLINE"}
    message_id, command_id = hub.new_ids()
    task_id = task_id or f"task_{uuid.uuid4().hex[:12]}"
    ok, err = hub.accept_command(
        session,
        command_id=command_id,
        task_id=task_id,
        action=action,
        args=args,
        deadline_ms=5000,
        generation=session.generation,
    )
    return {
        "ok": ok,
        "error_code": err,
        "command_id": command_id,
        "message_id": message_id,
        "task_id": task_id,
        "generation": session.generation,
        "action": action,
    }
