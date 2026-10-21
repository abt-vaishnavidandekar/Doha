from src.modules.enrollments.base.student.interface import Create_Enrollment, Check_seats
from src.modules.enrollments.base.student.models import Enrollment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.course.base.admin.models import Course
from src.modules.auth.student.models import Student
from src.modules.batch.base.admin.models import Batch
from src.modules.batch.base.admin.interface import Create_Batch
from src.configs.redis import seat_hold, seat_expiry, release_hold

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
            l1.append({
                "batch_id" : b.id, 
                "batch_name" : b.batch_name, 
                "Starting date":b.start_date, 
                "ending date" : b.end_date, 
                "from": b.starting_time, 
                "to" : b.ending_time, 
                "total seats" : b.seats, 
                "course_id" : b.course_id,
            }
            )


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True,
                "msg" : "Batches",
                "batch" : l1
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

        l2 = []

        for c in course: 
            l2.append({
                "course_id" : c.id, 
                "course_name" : c.name,
                "description" : c.description, 
                "overview" : c.overview}) 

        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Successfully getting the data",
                "course" : l2
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


async def available_seat(batch_id:int, current_user, db:AsyncSession):

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

    s = await db.execute(select(Enrollment).where(Enrollment.batch_id == batch_id))
    enroll = s.scalars().all()

    if enroll and batch:
        result = await db.execute(select(Enrollment).where(Enrollment.batch_id == batch_id))
        enrollment = result.scalars().all()

        count = 0

        for e in enrollment:
            count += 1
    


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "success" : True,
            "msg" : "Found the total number of seats available",
            "data" : {
                "batch_name" : batch.batch_name,
                "Total_seats" : batch.seats,
                "Available_seats" : batch.seats - count
            }
            
        }
    )



async def registration_hold_seat(batch_id: int, course_id: int, current_user, db: AsyncSession):

    try:

        student_id = current_user.id  

        result = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = result.scalar_one_or_none()

        if batch is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "msg" : "Batch Not found"
                }
            )

        result = await db.execute(select(Course).where(Course.id == course_id))
        course = result.scalar_one_or_none()

        if course is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "msg" : "Course Not found"
                }
            )

        s = await db.execute(select(Student).where(student_id == Student.id))

        student = s.scalar_one_or_none()

        if not (student and batch):
            result = await db.execute(select(Enrollment).where(Enrollment.student_id == student_id, Enrollment.batch_id == batch_id))
            enrollment = result.scalar_one_or_none()

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content = {
                    "success" : False,
                    "msg" : "Student with this id already registered for this Batch"
                }
            )  


        result = await seat_hold(batch_id, student_id, free_seats=(int(batch.seats) - 1))

        if result == 0:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content = {
                    "msg" : "No seats available"
                }
            )
        
        if result == student_id:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content = {
                    "msg" : "You already have a seat in this batch"
                }
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True, 
                "msg": "Seat held", 
                "expires_in": SESSION_EXPIRE,
            }
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error": str(e),
            },
        )
    


async def confirm_enrollment(batch_id: int, course_id: int, current_user, db: AsyncSession):

    student_id = current_user.id

    try:

        b = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = b.scalar_one_or_none()

        if batch is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "msg" : "Batch Not found"
                }
            )

        s = await db.execute(select(Student).where(student_id == Student.id))
        student = s.scalar_one_or_none()

        if not (student and batch):
            result = await db.execute(select(Enrollment).where(Enrollment.student_id == student_id, Enrollment.batch_id == batch_id))
            enrollment = result.scalar_one_or_none()

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content = {
                    "success" : False,
                    "msg" : "Student with this id already registered for this Batch"
                }
            )  

        if Enrollment.batch_id != batch_id:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : 'The batch id you have mentioned is not the same as registerd'
                }
            )

        if not seat_expiry:

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "msg" : "Seat hold expired"
                }
            )


        new_enrollment = Enrollment(
            student_id=student_id, 
            course_id=course_id, 
            batch_id=batch_id
        )

        db.add(new_enrollment)
        await db.commit()

        await release_hold(batch_id, student_id)  
        return {"success": True, "msg": "Enrolled successfully"}


    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error": str(e),
            },
        )