from src.configs.env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import UTC, datetime, timedelta
from jose import jwt


def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": datetime.now(UTC)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "refresh",
        "exp": datetime.now(UTC)
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
