import os
import time
import secrets

from src.configs.env import REDIS_URL, SESSION_EXPIRE
from redis.asyncio import Redis

from fastapi.responses import JSONResponse

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


async def get_redis() -> Redis:
    return redis_client


async def close_redis() -> None:
    await redis_client.aclose()


import time

async def hold_seat(batch_id: int, student_id: int, free_seats: int) -> int:
    now = time.time()

    lua_script = """
    local hold_key = KEYS[1]
    local now = tonumber(ARGV[1])
    local student_id = ARGV[2]
    local expire_at = tonumber(ARGV[3])
    local total_allowed_seats = tonumber(ARGV[4])

    -- 1. Clean up expired holds from the sorted set
    redis.call('ZREMRANGEBYSCORE', hold_key, '-inf', now)

    -- 2. Count active holds remaining
    local active_holds = redis.call('ZCARD', hold_key)

    -- 3. Check if we have room to add a new hold
    if active_holds < total_allowed_seats then
        -- Add/Update student hold with expiration timestamp as the score
        redis.call('ZADD', hold_key, expire_at, student_id)
        return 1
    else
        return 0
    end
    """
    
    result = await redis_client.eval(
        lua_script, 
        1, 
        f"batch:{batch_id}:holds",
        now, student_id, now + SESSION_EXPIRE, free_seats
    )
    
    return int(result)


async def release_hold(batch_id: int, student_id: int):
    await redis_client.zrem(f"batch:{batch_id}:holds", student_id)


async def seat_expiry(batch_id: int, student_id: int):
    await redis_client.zscore(f"batch:{batch_id}:holds", student_id)


async def hold_batch(batch_id : int, student_id:int):


    k = f"batch:{batch_id}:hold:{student_id}"

    success = await redis_client.set(
        k,
        student_id,
        ex=SESSION_EXPIRE,
        nx=True
    )

    if success is None:
        return {"msg" : "Batch already held"}

    return {
        "status" : "HELD",
        "timer" : await redis_client.ttl(k)
    }




async def seat_hold(batch_id : int, student_id:int):               #---------------------------------------> Seat holding logic


    key = f"batch:{batch_id}:hold:{student_id}"

    success = await redis_client.set(
        key,
        student_id,
        ex=SESSION_EXPIRE,
        nx=True
    )

    if success is None:
        return {"msg" : "Batch already held"}

    return {
        "status" : "HELD",
        "timer" : await redis_client.ttl(key)
    }









    

    


    