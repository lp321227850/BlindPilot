from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

from app.safety.engine import SafetyEngine


@dataclass
class DeviceSession:
    device_id: str
    token: str
    generation: int = 0
    seen_commands: set[str] = field(default_factory=set)
    cancelled_tasks: set[str] = field(default_factory=set)
    last_seen: float = field(default_factory=time.time)


class DeviceHub:
    def __init__(self, safety: SafetyEngine | None = None) -> None:
        self.safety = safety or SafetyEngine()
        self.sessions: dict[str, DeviceSession] = {}
        self.tokens: dict[str, str] = {}

    def register(self, device_id: str, token: str) -> DeviceSession:
        session = DeviceSession(device_id=device_id, token=token)
        self.sessions[device_id] = session
        self.tokens[device_id] = token
        return session

    def authenticate(self, device_id: str, token: str) -> DeviceSession | None:
        expected = self.tokens.get(device_id)
        if expected is None or expected != token:
            return None
        session = self.sessions.get(device_id) or self.register(device_id, token)
        session.last_seen = time.time()
        return session

    def cancel_task(self, device_id: str, task_id: str) -> None:
        session = self.sessions.get(device_id)
        if session is None:
            return
        session.cancelled_tasks.add(task_id)
        session.generation += 1

    def local_stop(self, device_id: str) -> int:
        session = self.sessions.get(device_id)
        if session is None:
            return 0
        session.generation += 1
        return session.generation

    def accept_command(
        self,
        session: DeviceSession,
        command_id: str,
        task_id: str,
        action: str,
        args: dict,
        deadline_ms: int,
        generation: int,
        sent_at_ms: int | None = None,
    ) -> tuple[bool, str | None]:
        now_ms = int(time.time() * 1000)
        sent_at_ms = sent_at_ms or now_ms
        if now_ms - sent_at_ms > deadline_ms:
            return False, "STALE_COMMAND"
        if command_id in session.seen_commands:
            return False, "STALE_COMMAND"
        if task_id in session.cancelled_tasks:
            return False, "TASK_CANCELLED"
        if generation != session.generation:
            return False, "STALE_COMMAND"
        decision = self.safety.classify(action, args)
        if not decision.allowed:
            session.seen_commands.add(command_id)
            return False, decision.error_code or "BLOCKED_BY_POLICY"
        session.seen_commands.add(command_id)
        session.last_seen = time.time()
        return True, None

    def new_ids(self) -> tuple[str, str]:
        return f"msg_{uuid.uuid4().hex[:12]}", f"cmd_{uuid.uuid4().hex[:12]}"
