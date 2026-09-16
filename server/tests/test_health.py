from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_live():
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_ready_does_not_require_agent():
    r = client.get("/health/ready")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["agent_configured"] is False


def test_agent_demo_is_unavailable_without_key():
    r = client.post("/v1/agent/observe-demo")
    assert r.status_code == 503
    assert "Antigravity" in r.json()["detail"]
    assert "Gemini" in r.json()["detail"] or "OpenAI" in r.json()["detail"]
