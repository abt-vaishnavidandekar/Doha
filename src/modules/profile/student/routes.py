from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.profile.student.functions import get_student_detail, update_student_datails
from src.modules.profile.student.interface import Update_Student

profile_router = APIRouter(tags=["Profile-2"])

@profile_router.get("/get_student")
async def get_admin(email : str, db:AsyncSession=Depends(get_db)):
    return await get_student_detail(email= email, db=db)


@profile_router.put("/update/{student_id}")
async def update_admin(data : Update_Student, db:AsyncSession=Depends(get_db)):
    return await update_student_datails(data=data, db=db)