from __future__ import annotations

import secrets
import time
from dataclasses import dataclass


@dataclass
class PairingCode:
    code: str
    expires_at: float
    used: bool = False


class PairingStore:
    def __init__(self, ttl_seconds: int = 600) -> None:
        self.ttl = ttl_seconds
        self._codes: dict[str, PairingCode] = {}
        self.devices: dict[str, dict] = {}

    def start(self) -> PairingCode:
        code = secrets.token_hex(3).upper()
        item = PairingCode(code=code, expires_at=time.time() + self.ttl)
        self._codes[code] = item
        return item

    def complete(self, code: str, display_name: str, public_key: str | None = None) -> dict | None:
        item = self._codes.get(code.upper().strip())
        if item is None or item.used or item.expires_at < time.time():
            return None
        item.used = True
        device_id = f"dev_{secrets.token_hex(8)}"
        token = secrets.token_urlsafe(32)
        record = {
            "device_id": device_id,
            "device_token": token,
            "display_name": display_name,
            "public_key": public_key,
        }
        self.devices[device_id] = record
        return record
