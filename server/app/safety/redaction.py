PROTECTED = "[PROTECTED]"

SECRET_KEYS = ("password", "otp", "pin", "cvv", "secret", "token_plain")


def is_secret_node(node: dict) -> bool:
    if node.get("password") or node.get("role") == "password_field":
        return True
    rid = str(node.get("resource_id") or "").lower()
    return any(k in rid for k in ("password", "otp", "pay_pwd", "cvv"))


def redact_node(node: dict) -> dict:
    out = dict(node)
    if is_secret_node(out):
        out["text"] = PROTECTED
        out["value"] = PROTECTED
        out["content_description"] = PROTECTED
        out["role"] = "password_field"
    return out


def redact_screen_state(state: dict) -> dict:
    nodes = [redact_node(n) for n in state.get("nodes") or []]
    out = dict(state)
    out["nodes"] = nodes
    return out


def contains_secret_plaintext(payload: object) -> bool:
    if payload is None:
        return False
    if isinstance(payload, str):
        return False
    if isinstance(payload, dict):
        if is_secret_node(payload):
            text = str(payload.get("text") or payload.get("value") or "")
            return bool(text) and text != PROTECTED
        return any(contains_secret_plaintext(v) for v in payload.values())
    if isinstance(payload, list):
        return any(contains_secret_plaintext(v) for v in payload)
    return False
