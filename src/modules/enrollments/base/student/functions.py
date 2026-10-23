from src.modules.enrollments.base.student.interface import Create_Enrollment, Check_seats
from src.modules.enrollments.base.student.models import Enrollment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.course.base.admin.models import Course
from src.modules.auth.student.models import Student
from src.modules.batch.base.admin.models import Batch
from src.modules.batch.base.admin.interface import Create_Batch
from src.configs.redis import seat_hold, seat_expiry, release_hold, get_seat_hold, count_batch_holds

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

    count = len(enroll)
    held_count = await count_batch_holds(batch_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "success" : True,
            "msg" : "Found the total number of seats available",
            "data" : {
                "batch_name" : batch.batch_name,
                "Total_seats" : batch.seats,
                "Available_seats" : max(0, batch.seats - count - held_count)
            }
            
        }
    )



async def registration_hold_seat(batch_id: int, course_id: int, current_user, db: AsyncSession):

    student_id = current_user.id

    try:

        result = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = result.scalar_one_or_none()

        if batch is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batch Not found"
                }
            )

        result = await db.execute(select(Batch).where(Batch.id == batch_id, Batch.course_id == course_id))
        course = result.scalar_one_or_none()

        if course is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Course Not found"
                }
            )

        s = await db.execute(select(Student).where(student_id == Student.id))
        student = s.scalar_one_or_none()

        if student is None:
            return JSONResponse(
                status_code= status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Student Not found"
                }
            )

        result = await db.execute(select(Enrollment).where(Enrollment.student_id == student_id, Enrollment.batch_id == batch_id, Enrollment.course_id == course_id))
        existing = result.scalar_one_or_none()

        if existing:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "success" : False,
                    "msg" : "Student already enrolled in this batch and course"
                }
            )

        result = await db.execute(select(Enrollment).where(Enrollment.batch_id == batch_id))
        enrollments = result.scalars().all()

        count = len(enrollments)
        held_count = await count_batch_holds(batch_id)

        if count + held_count >= batch.seats:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "success": False,
                    "msg": "No seats available for enrollment.",
                },
            )

        result = await seat_hold(student_id, batch_id)

        if not result:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "success": False,
                    "msg": "You already have an active seat hold",
                },
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True, 
                "msg": "Seat held successfully", 
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
        batch = b.scalars().all()

        if batch is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batch Not found"
                }
            )

        l1 = []
        for i in batch:
            l1.append({
                "batch_id" : i.id, 
                "batch_name" : i.batch_name, 
                "date" : f"{i.start_date} to {i.end_date}",
                "time": f"{i.starting_time} to {i.ending_time}",
            })


        result = await db.execute(select(Batch).where(Batch.id == batch_id, Batch.course_id == course_id))
        course = result.scalar_one_or_none()
        
        if course is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "This course doesn't belongs to the selected batch"
                }
            )

        c = await db.execute(select(Course).where(Course.id == course_id))
        course = c.scalars().all()   
        
        l2 = []
        for c in course:
                l2.append({
                "course_id" : c.id, 
                "course_name" : c.name,
                "description" : c.description, 
                "overview" : c.overview
                }) 

        held_batch = await get_seat_hold(current_user.id)

        if held_batch is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "Hold a seat first, or hold expire"
                }
            )

        if held_batch != str(batch_id):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content = {
                    "success" : False,
                    "msg" : "Your hold belongs to another batch"
                }
            )


        result = await db.execute(select(Student).where(Student.id == current_user.id))
        student = result.scalars().all()

        l3 = []
        for i in student:
            l3.append({
                "id" : i.id,
                "name" : f"{i.first_name} {i.last_name}",
                "email" : i.email,
                "ph_no" : i.ph_no

            })

        result = await db.execute(select(Enrollment).where(Enrollment.student_id == student_id, Enrollment.batch_id == batch_id))
        existing = result.scalar_one_or_none()

        if existing:
            await release_hold(student_id)

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "success": False,
                    "msg": "Student is already enrolled in this batch.",
                },
            )

        result = await db.execute(select(Enrollment).where(Enrollment.batch_id == batch_id))
        enrollments = result.scalars().all()

        count = len(enrollments)
        held_count = await count_batch_holds(batch_id)

        result = await db.execute(select(Batch).where(batch_id == Batch.id))
        batch = result.scalar_one_or_none()

        if count + held_count > batch.seats:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "success": False,
                    "msg": "No seats available for enrollment.",
                },
            )


        new_enrollment = Enrollment(
            student_id=student_id, 
            course_id=course_id, 
            batch_id=batch_id
        )

        db.add(new_enrollment)
        await db.commit()

        await release_hold(student_id)  


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Enrolled successfully",
                "student_deatils" : l3,
                "batch_details": l1,
                "course_details": l2,
            },
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