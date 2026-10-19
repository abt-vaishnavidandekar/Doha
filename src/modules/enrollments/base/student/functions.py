from src.modules.enrollments.base.student.interface import Create_Enrollment, Check_seats
from src.modules.enrollments.base.student.models import Enrollment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.course.base.admin.models import Course
from src.modules.auth.student.models import Student
from src.modules.batch.base.admin.models import Batch
from src.modules.batch.base.admin.interface import Create_Batch

from fastapi import status
from fastapi.responses import JSONResponse

SESSION_EXPIRE = 10*60  
    

async def get_batches(current_user, db:AsyncSession):

    try:
        result = await db.execute(select(Batch))
        batch = result.scalars().all()

        if not batch:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batches doesn't exists!"
                }
            )

        l1 = []

        for b in batch:
            l1.extend([b.id, b.batch_name, b.start_date, b.end_date, b.starting_time, b.ending_time, b.seats, b.course_id])


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True,
                "msg" : "Batches",
                "batch" : {
                    "batch_id" : batch.id,
                }
            },
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )
    


async def get_courses(current_user, db:AsyncSession):
    
    try:
        result = await db.execute(select(Course))
        course = result.scalars().all()

        if not course:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Course not found"
                }
            )

        l1 = []

        for c in course: 
            l1.extend([c.id, c.name, c.description, c.overview]) 

        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Successfully getting the data",
                "course" : l1
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


async def check_seats(batch_id:int, db:AsyncSession):

    try:
        result = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = result.scalar_one_or_none()

        if not batch:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "batch with this id doesn't exists"
                }
            )


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Found the total number of seats available",
                "data" : {
                    "batch_name" : batch.batch_name,
                    "available_seats" : batch.seats,
                }
                
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "Error":print(e)
            },
        )



async def enroll_for_course(data : Create_Enrollment, current_user, db:AsyncSession):   #hold until verified successfully

    try:
        student_exists = db.get(Student, data.student_id)
        if not student_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Course with this id doesn't exists"
                }
            )

        batch_exists = db.get(Batch, data.batch_id)
        if not batch_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Course with this id doesn't exists"
                }
            )
        
        course_exists = db.get(Course, data.course_id)
        if not course_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Course with this id doesn't exists"
                }
            )

        new_enrollment = Enrollment(
            student_id = data.student_id,
            course_id = data.course_id,
            batch_id = data.batch_id
        )


        db.add(new_enrollment)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : False,
                "msg" : "Enrolled successfully for the batch and course",
            }
        )


    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error": str(e),
            },
        )


async def confirm_enrollment(email : str, code:str, db:AsyncSession):
    #Redis generate code --> code verify : if verified Successfully enrolled successfully seat confirm else release

    try:
        result = await db.execute(select(Student).where(Student.email == email))
        student = result.scalar_one_or_none()

        if not student:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Not found --> use registered email"
                }
            )



    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error": str(e),
            },
        )