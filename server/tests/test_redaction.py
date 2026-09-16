from app.safety.redaction import PROTECTED, contains_secret_plaintext, redact_screen_state


def test_password_node_redacted():
    state = {
        "package": "com.example",
        "nodes": [
            {"id": "n1", "role": "password_field", "text": "hunter2", "password": True},
            {"id": "n2", "role": "button", "text": "登录"},
        ],
    }
    out = redact_screen_state(state)
    assert out["nodes"][0]["text"] == PROTECTED
    assert out["nodes"][1]["text"] == "登录"
    assert not contains_secret_plaintext(out)
    assert contains_secret_plaintext(state)
