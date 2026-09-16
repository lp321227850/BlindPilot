from enum import StrEnum


class RiskLevel(StrEnum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"
    SECRET = "SECRET"


GREEN_TOOLS = {
    "phone_observe",
    "phone_back",
    "phone_home",
    "phone_scroll",
    "phone_swipe",
    "phone_open_app",
    "phone_wait",
    "phone_finish",
    "phone_abort",
    "phone_ask_user",
}

YELLOW_TOOLS = {
    "phone_click",
    "phone_long_click",
    "phone_set_text",
}

RED_TOOLS = {
    "dpm_wipe",
    "dpm_uninstall",
    "dpm_install",
    "factory_reset",
    "phone_shell",
    "phone_intent",
    "phone_http",
}

YELLOW_CLICK_HINTS = (
    "发送",
    "send",
    "拨打",
    "呼叫",
    "call",
    "视频",
    "语音通话",
    "支付",
    "购买",
    "删除",
    "卸载",
    "转账",
)

RED_CLICK_HINTS = (
    "转账",
    "付款",
    "支付",
    "确认付款",
    "购买",
    "卸载",
    "恢复出厂",
    "wipe",
    "factory reset",
)
