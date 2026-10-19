from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.role import get_current_admin

from src.configs.database import get_db
from src.modules.batch.base.admin.functions import create_batch, get_batch, update_batch, delete_batch
from src.modules.batch.base.admin.interface import Create_Batch, Update_Batch

batch_router = APIRouter(tags=["Batch"])

@batch_router.post("/batch")
async def register(data: Create_Batch, current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await create_batch(data=data, current_user=current_user, db=db)

@batch_router.get("/batch")
async def get_batches(current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await get_batch(current_user=current_user, db=db)

@batch_router.put("/batch/{batch_id}")
async def update(batch_id:int, data: Update_Batch, current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await update_batch(batch_id=batch_id, data=data, current_user=current_user, db=db)

@batch_router.delete("/batch/{batch_id}")
async def delete_bt(batch_id:int, current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await delete_batch(batch_id=batch_id, current_user=current_user, db=db)