from fastapi import Cookie, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.auth.admin.models import Admin
from src.modules.auth.student.models import Student
from src.configs.env import SECRET_KEY, ALGORITHM

async def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not access_token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
                detail={"success" : False,
                        "msg" : "Access token missing"}) 
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, 
                detail={"success" : False,
                        "msg" :"Invalid Access token"})

        user_id = int(payload["sub"])
        role = payload.get("role")
        if role not in ("student", "admin"):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, 
                detail={"success" : False,
                        "msg" :"Invalid role"})

    except (JWTError, ValueError, KeyError, TypeError):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            detail={"success" : False,
                    "msg" :"Invalid or expired access token"}
                )

    model = Admin if role == "admin" else Student
    result = await db.execute(select(model).where(model.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            detail={"success" : False,
                    "msg" :"User not found"})
    return user


async def get_current_admin(current_user = Depends(get_current_user)):
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, 
            detail={"success" : False,
                    "msg" :"Admin access required"})
    return current_user


async def get_current_student(current_user = Depends(get_current_user)):
    if not isinstance(current_user, Student):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, 
            detail={"success" : False,
                    "msg" :"Unauthorized, access required"})
    return current_user