from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.enrollments.base.student.models import Enrollment
from src.modules.enrollments.base.admin.interface import Update_Enrollment

from src.utils.validations import check_date, check_time


async def get_enrollments(current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Enrollment))
        enrollment = result.scalars().all()

        if not enrollment:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Enrollments not found"
                }
            )

        l1 = []

        for e in enrollment:
            l1.append({
                "enrollment_id" : e.id,
                "student_id" : e.student_id,
                "batch_id" : e.batch_id,
                "course_id" : e.course_id,
            })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True,
                "msg" : "Data successfully getting",
                "enrollment" : l1

            },
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "errors" : str(e)
            },
        )

async def update_enrollments(enrollment_id: int, data: Update_Enrollment,current_user, db: AsyncSession):

    try:
        result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
        enrollment = result.scalar_one_or_none()

        if enrollment is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Enrollments not found"
            }
        )

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(enrollment, field, value)

        await db.commit()
        await db.refresh(enrollment)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success" : False,
                "msg" : "Enrollment successfully updated",
                "enrollments" : enrollment
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )


async def delete_enrollments(enrollment_id : int, current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
        enrollment = result.scalar_one_or_none()

        if not enrollment:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batch not found"
                }
            )

        db.delete(enrollment)
        await db.refresh(enrollment)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Enrollment successfully deleted"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )