# BlindPilot server

FastAPI process that terminates behind Caddy.

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"   # Windows: .venv\Scripts\pip
.venv/bin/pytest
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Health:

- `GET /health/live`
- `GET /health/ready` — ready even if Antigravity is not configured

Agent runtime is Antigravity only. An unconfigured key returns HTTP 503, never a second provider.
