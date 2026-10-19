from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.enrollments.base.student.interface import Create_Enrollment, Check_seats
from src.modules.batch.base.admin.interface import Create_Batch

from src.configs.database import get_db
from src.utils.role import get_current_student


from src.modules.enrollments.base.student.functions import check_seats, get_batches, get_courses, enroll_for_course

enrollment_router = APIRouter(tags=["Enrollment"])

@enrollment_router.get("/enrollments/seats")
async def seats(batch_id:int, db:AsyncSession= Depends(get_db)):
    return await check_seats(batch_id=batch_id, db=db)


@enrollment_router.get("/view-Batch")
async def get_data1(current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await get_batches(current_user=current_user, db=db)

@enrollment_router.get("/view-Course")
async def get_data2(current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await get_courses(current_user=current_user, db=db)

@enrollment_router.post("/enrollment")
def enroll(data : Create_Enrollment, current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return enroll_for_course(data=data, current_user=current_user, db=db)
