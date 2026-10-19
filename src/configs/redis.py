import os
import secrets

from src.configs.env import REDIS_URL, CODE_LENGTH, CODE_ATTEMPT, CODE_EXPIRY
from redis.asyncio import Redis



REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


async def get_redis() -> Redis:
    return redis_client


async def close_redis() -> None:
    await redis_client.aclose()


def generate_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(length))


async def create_email_code(email:str) -> str:
    code = generate_code()

    await redis_client.set(f"email_code:{email}", code, ex=CODE_EXPIRY)
    await redis_client.delete(f"code_attempts:{email}") 

    return code

