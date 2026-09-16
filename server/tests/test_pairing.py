from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_expired_or_wrong_code_fails():
    r = client.post("/v1/pair/complete", json={"pairing_code": "NOPE00", "display_name": "x"})
    assert r.status_code == 400
