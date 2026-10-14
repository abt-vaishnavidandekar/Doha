from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.profile.admin.functions import get_admin_detail, update_admin_datails
from src.modules.profile.admin.interface import Update_Admin
from src.utils.role import get_current_user

profile_router = APIRouter(tags=["Profile-1"])

@profile_router.get("/get_admin/{user_id}")
async def get_admin(user_id:int, db:AsyncSession=Depends(get_db)):
    return await get_admin_detail(user_id=user_id, db=db)


@profile_router.put("/update/{user_id}")
async def update_admin(data : Update_Admin, db:AsyncSession=Depends(get_db)):
    return await update_admin_datails(data=data, db=db)

