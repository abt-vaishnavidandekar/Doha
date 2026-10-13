from sqlalchemy.ext.asyncio import AsyncSession
from src.configs.database import get_db
from fastapi import APIRouter, Depends
from src.modules.auth.admin.models import Admin
from src.modules.auth.admin.interface import Create_Admin, Admin_login
from src.modules.auth.admin.functions import register_admin, login_admin, logout

from fastapi.responses import Response

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