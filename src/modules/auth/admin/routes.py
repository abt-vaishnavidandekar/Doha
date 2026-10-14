from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy import select
from src.utils.jwt import SECRET_KEY, ALGORITHM, create_access_token, create_refresh_token
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from src.modules.auth.admin.models import Admin
from src.modules.auth.student.models import Student

from src.configs.database import get_db
from src.modules.auth.admin.functions import (
    login_admin,
    logout,
    register_admin,
)
from src.modules.auth.admin.interface import Admin_login, Create_Admin

admin_router = APIRouter(tags=["Admin"])


@admin_router.post("/register")
async def admin_register(data: Create_Admin, db: AsyncSession = Depends(get_db)):
    return await register_admin(data=data, db=db)

@admin_router.post("/login")
async def admin_login(data: Admin_login, response:Response, db : AsyncSession=Depends(get_db)):
    return await login_admin(data=data, response=response, db=db)

@admin_router.post("/logout")
async def logout_admin(response : Response):
    return await logout(response=response)


@admin_router.post("/refresh")
async def refresh_access_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token cookie missing",
        )

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        user_id = int(payload["sub"])
        role = payload.get("role")

        if role not in ("admin", "student"):
            raise HTTPException(
                status_code=401,
                detail="Invalid user role",
            )

    except (JWTError, ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )

    model = Admin if role == "admin" else Student

    result = await db.execute(
        select(model).where(model.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    new_access_token = create_access_token(user.id, role)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=15 * 60,
        path="/",
    )

    return {"message": "Access token refreshed"}