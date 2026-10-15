from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.enrollments.base.student.interface import Create_Enrollment, Update_Enrollment
from src.modules.enrollments.base.admin.functions import get_enrollments, update_enrollments, delete_enrollments
from src.utils.role import get_current_admin

enrollment_router = APIRouter(tags=["Enrollment"])


@enrollment_router.get("/get_enrollment")
async def get_enrolls(current_user=Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await get_enrollments(current_user=current_user, db=db)

@enrollment_router.patch("/update_enrollment/{enrollment_id}")
async def update_enrolls(enrollment_id: int, data: Update_Enrollment, current_user = Depends(get_current_admin), db: AsyncSession = Depends(get_current_admin)):
    return await update_enrollments(enrollment_id=enrollment_id, data=data, current_user=current_user, db=db)

@enrollment_router.delete("/delete_enrollment/{enrollment_id}")
async def delete_enrolls(enrollment_id : int, current_user=Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await delete_enrollments(enrollment_id=enrollment_id, current_user=current_user, db=db)