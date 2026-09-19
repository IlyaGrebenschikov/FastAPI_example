import redis.asyncio as aioredis


def create_client(url: str) -> aioredis.Redis:
    return aioredis.from_url(url)
