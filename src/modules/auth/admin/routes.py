from fastapi import APIRouter, Depends
from src.utils.role import get_current_admin
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from src.configs.database import get_db
from src.modules.auth.admin.functions import (
    login_admin,
    logout,
    register_admin,
    refresh_access_token
)
from src.modules.auth.admin.interface import Admin_login, Create_Admin

admin_router = APIRouter(tags=["Admin"])


@admin_router.post("/register")
async def admin_register(data: Create_Admin, db: AsyncSession = Depends(get_db)):
    return await register_admin(data=data, db=db)

@admin_router.post("/login")
async def admin_login(data: Admin_login, token:Request, db : AsyncSession=Depends(get_db)):
    return await login_admin(data=data, db=db)

@admin_router.post("/logout")
async def logout_admin(current_user=Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await logout(current_user=current_user, db=db)

@admin_router.post("/refresh")
async def refresh_the_token(refresh_token : Request):
    return refresh_access_token(refresh_token=refresh_token)