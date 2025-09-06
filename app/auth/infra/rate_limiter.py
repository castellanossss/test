class NoopRateLimiter:
    async def check(self, key: str) -> None:
        return
