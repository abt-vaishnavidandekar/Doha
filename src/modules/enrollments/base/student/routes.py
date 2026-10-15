from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.enrollments.base.student.interface import Create_Enrollment
from src.modules.enrollments.base.student.functions import create_enrollments
from src.utils.role import get_current_user

enrollment_router = APIRouter(tags=["Enrollment"])

@enrollment_router.post("/register_enrollment")
async def register(data: Create_Enrollment, current_user=Depends(get_current_user), db:AsyncSession=Depends(get_db)):
    return await create_enrollments(data=data, current_user=current_user, db=db)

