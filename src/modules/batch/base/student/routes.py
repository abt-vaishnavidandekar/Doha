from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.role import get_current_student

from src.configs.database import get_db
from src.modules.batch.base.admin.functions import create_batch, get_batch, update_batch

batch_router = APIRouter(tags=["Batch"])


@batch_router.get("/get_batch")
async def get_batches(current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await get_batch(current_user=current_user, db=db)

