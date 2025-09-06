from app.auth.domain.interfaces import AuditRepository

class InMemoryAuditRepo(AuditRepository):
    def __init__(self):
        self._events: list[tuple[str|None, str, dict|None]] = []

    async def log_event(self, actor_id: str | None, action: str, data: dict | None = None) -> None:
        self._events.append((actor_id, action, data or {}))
