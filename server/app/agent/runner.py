class AgentNotConfigured(RuntimeError):
    """Runtime cloud AI is Antigravity only. No generateContent fallback exists."""


class AgentRunner:
    """v1 runtime: Antigravity Agent only. Never OpenAI/Gemini/Grok/Anthropic."""

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key.strip()

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    async def start_observe_task(self, user_text: str) -> dict:
        if not self.available:
            raise AgentNotConfigured(
                "Antigravity Agent is not configured. BlindPilot will not fall back to Gemini or OpenAI.",
            )
        raise AgentNotConfigured("Antigravity Agent wiring is M5; key present but runner not implemented yet.")
