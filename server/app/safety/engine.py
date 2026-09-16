from app.safety.policy import (
    GREEN_TOOLS,
    RED_CLICK_HINTS,
    RED_TOOLS,
    YELLOW_CLICK_HINTS,
    YELLOW_TOOLS,
    RiskLevel,
)
from app.safety.redaction import is_secret_node


class SafetyDecision:
    def __init__(self, level: RiskLevel, allowed: bool, reason: str, error_code: str | None = None):
        self.level = level
        self.allowed = allowed
        self.reason = reason
        self.error_code = error_code


class SafetyEngine:
    """Deterministic policy. Not an LLM prompt."""

    def classify(self, tool_name: str, arguments: dict | None = None) -> SafetyDecision:
        args = arguments or {}
        tool = (tool_name or "").strip()

        if tool in RED_TOOLS or tool.startswith("adb") or "shell" in tool:
            return SafetyDecision(RiskLevel.RED, False, "v1 blocks destructive/system tools", "BLOCKED_BY_POLICY")

        if args.get("secret") or is_secret_node(args) or args.get("role") == "password_field":
            return SafetyDecision(RiskLevel.SECRET, False, "SECRET field never sent to Agent", "SECRET_FIELD")

        if tool == "phone_set_text" and (
            args.get("password") or str(args.get("node_role") or "") == "password_field"
        ):
            return SafetyDecision(RiskLevel.SECRET, False, "cannot cloud-fill SECRET fields", "SECRET_FIELD")

        label = " ".join(
            str(args.get(k) or "")
            for k in ("text", "content_description", "node_text", "app_name", "summary")
        ).lower()

        if any(h.lower() in label for h in RED_CLICK_HINTS) and tool in {"phone_click", "phone_long_click"}:
            return SafetyDecision(RiskLevel.RED, False, "financial/destructive click blocked in v1", "BLOCKED_BY_POLICY")

        if tool in GREEN_TOOLS:
            return SafetyDecision(RiskLevel.GREEN, True, "navigation/read is automatic", None)

        if tool in YELLOW_TOOLS:
            if any(h.lower() in label for h in YELLOW_CLICK_HINTS):
                return SafetyDecision(
                    RiskLevel.YELLOW,
                    False,
                    "consequential action needs confirmation",
                    "CONFIRMATION_REQUIRED",
                )
            if tool == "phone_set_text":
                return SafetyDecision(RiskLevel.GREEN, True, "ordinary text input", None)
            return SafetyDecision(RiskLevel.GREEN, True, "ordinary click", None)

        return SafetyDecision(RiskLevel.RED, False, f"unknown tool {tool}", "ACTION_NOT_SUPPORTED")
