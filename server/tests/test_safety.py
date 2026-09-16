from app.safety.engine import SafetyEngine
from app.safety.policy import RiskLevel

engine = SafetyEngine()


def test_observe_is_green():
    d = engine.classify("phone_observe", {"mode": "COMPACT"})
    assert d.level == RiskLevel.GREEN
    assert d.allowed is True


def test_open_app_is_green():
    d = engine.classify("phone_open_app", {"app_name": "设置"})
    assert d.allowed is True
    assert d.level == RiskLevel.GREEN


def test_send_click_is_yellow():
    d = engine.classify("phone_click", {"text": "发送"})
    assert d.level == RiskLevel.YELLOW
    assert d.allowed is False
    assert d.error_code == "CONFIRMATION_REQUIRED"


def test_payment_click_is_red():
    d = engine.classify("phone_click", {"text": "确认付款"})
    assert d.level == RiskLevel.RED
    assert d.allowed is False
    assert d.error_code == "BLOCKED_BY_POLICY"


def test_wipe_is_red():
    d = engine.classify("dpm_wipe", {})
    assert d.level == RiskLevel.RED
    assert d.allowed is False


def test_password_set_text_is_secret():
    d = engine.classify("phone_set_text", {"password": True, "text": "123456"})
    assert d.level == RiskLevel.SECRET
    assert d.allowed is False
    assert d.error_code == "SECRET_FIELD"


def test_unknown_tool_blocked():
    d = engine.classify("phone_shell", {"cmd": "id"})
    assert d.allowed is False
