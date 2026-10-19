from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.profile.admin.functions import get_admin_detail, update_admin_details
from src.modules.profile.admin.interface import Update_Admin
from src.utils.role import get_current_admin

profile_router = APIRouter(tags=["Profile-1"])

@profile_router.get("/admin")
async def get_admin(user_id:int, current_user=Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await get_admin_detail(user_id = user_id, current_user=current_user, db=db)


@profile_router.put("/admin/{user_id}")
async def update_admin(data : Update_Admin, current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await update_admin_details(data=data, current_user=current_user, db=db)

