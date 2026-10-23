import os

from src.configs.env import REDIS_URL, SESSION_EXPIRE
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


async def seat_hold(student_id: int, batch_id: int):
    key = f"seat_lock:{student_id}"

    result = await redis_client.set(
        key,
        batch_id,
        nx=True,
        ex=SESSION_EXPIRE,
    )

    return bool(result)


async def get_seat_hold(student_id: int) -> int:
    return await redis_client.get(f"seat_lock:{student_id}")


async def release_hold(student_id: int) -> int:
    return await redis_client.delete(f"seat_lock:{student_id}")


async def seat_expiry(student_id: int):
    remaining = await redis_client.ttl(f"seat_lock:{student_id}")
    return max(0, remaining)


async def count_batch_holds(batch_id: int):
    count = 0

    async for key in redis_client.scan_iter(match="seat_lock:*"):
        held_batch = await redis_client.get(key)

        if held_batch == str(batch_id):
            count += 1

    return count







    

    


    