from src.modules.enrollments.base.student.interface import Create_Enrollment
from src.modules.enrollments.base.student.models import Enrollment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.course.base.admin.models import Course
from src.modules.auth.student.models import Student
from src.modules.batch.base.admin.models import Batch

from fastapi import status
from fastapi.responses import JSONResponse


async def create_enrollments(data:Create_Enrollment, current_user, db:AsyncSession):

    try:
        course_exists = await db.get(Course, data.course_id)
        if not course_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Course with this id doesn't exists"
                }
            )

        student_exists = await db.get(Student, data.student_id)
        if not student_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg"  : "Student with this id Does't exists"
                }
            )

        batch_exists = await db.get(Batch, data.batch_id)
        if not batch_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg"  : "Batch with this id Does't exists"
                }
            )


        enrollment = Enrollment(
            course_id = data.course_id,
            student_id = data.student_id,
            batch_id = data.batch_id
        )

        db.add(enrollment),
        await db.commit()
        await db.refresh(enrollment)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content = {
                "success" : True,
                "msg" : "Successfully enrolled"
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
      




