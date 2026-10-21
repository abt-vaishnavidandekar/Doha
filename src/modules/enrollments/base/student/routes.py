from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.enrollments.base.student.interface import Create_Enrollment, Check_seats
from src.modules.batch.base.admin.interface import Create_Batch

from src.configs.database import get_db
from src.utils.role import get_current_student


from src.modules.enrollments.base.student.functions import available_seat, get_batches, get_courses, registration_hold_seat, confirm_enrollment

enrollment_router = APIRouter(tags=["Enrollment"])


@enrollment_router.get("/view-Batch")
async def get_data1(current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await get_batches(current_user=current_user, db=db)

@enrollment_router.get("/view-Course")
async def get_data2(current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await get_courses(current_user=current_user, db=db)

@enrollment_router.post("/enrollment")
async def seats_available(batch_id:int, current_user = Depends(get_current_student), db:AsyncSession= Depends(get_db)):
    return await available_seat(batch_id=batch_id, current_user=current_user, db=db)


@enrollment_router.post("/enrollment/hold")
async def hold_seat_for_student(batch_id: int, course_id: int, current_user = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await registration_hold_seat(batch_id=batch_id, course_id=course_id, current_user=current_user, db=db)


@enrollment_router.post("/enrollment/hold")
async def enrollment(batch_id: int, course_id: int, current_user = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await confirm_enrollment(batch_id=batch_id, course_id=course_id, current_user=current_user, db=db)