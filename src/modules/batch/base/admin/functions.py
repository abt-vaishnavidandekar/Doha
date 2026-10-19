from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.batch.base.admin.interface import Create_Batch, Update_Batch
from src.modules.batch.base.admin.models import Batch
from src.modules.course.base.admin.models import Course

from src.utils.validations import check_date, check_time


async def create_batch(data: Create_Batch, current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Batch).where(Batch.batch_name == data.batch_name ))
        batch = result.scalar_one_or_none()

        if batch:
            return JSONResponse(
                status_code= status.HTTP_409_CONFLICT,
                content = {
                    "success" : False,
                    "msg" : "Batch with this name already exists"
                }
            )

        course_exists = await db.get(Course, data.course_id)
        if not course_exists:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Course with this id doesn't exists"
                }
            )

        if check_date(data.start_date) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "Enter a valid date form yyyy:mm:dd"
                }
            )

        if check_date(data.end_date) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "Enter a valid date form yyyy:mm:dd"
                }
            )


        if check_time(data.starting_time) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "Enter a valid time form HH:MM:SS"
                }
            )       

        if check_time(data.ending_time) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "Enter a valid time form HH:MM:SS"
                }
            )       
        

        if data.end_date <= data.start_date:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "msg": "Ending date must be after starting date",
                },
            )
        

        batch = Batch(
            batch_name = data.batch_name,
            start_date = data.start_date,
            end_date = data.end_date,
            starting_time = data.starting_time, 
            ending_time = data.ending_time,
            seats = data.seats,
            course_id = data.course_id
        )

        db.add(batch)
        await db.commit()
        await db.refresh(batch)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content = {
                "success" : True,
                "msg" : "Successfully created Batch"}
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



async def get_batch(current_user, db:AsyncSession):

    try:
        result = await db.execute(select(Batch))
        batch = result.scalars().all()

        if not batch:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batches doen't exists!"
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
                "batch" : l1,
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



async def update_batch(
    batch_id: int,
    data: Update_Batch,
    current_user,
    db: AsyncSession,
):
    try:
        result = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = result.scalar_one_or_none()

        if not batch:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, 
                    "msg": "Batch not found",
                    }
            )

        if not check_date(data.start_date) or not check_date(data.end_date):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False,
                    "msg": "Invalid date format",
                    }
            )

        if not check_time(data.starting_time) or not check_time(data.ending_time):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Invalid time format"},
            )

        if data.end_date <= data.start_date:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "msg": "Ending date must be after starting date",
                },
            )

        if not await db.get(Course, data.course_id):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Course not found"},
            )

        batch.batch_name = data.batch_name
        batch.startdate = data.start_date
        batch.end_date = data.end_date
        batch.starting_time = data.starting_time
        batch.ending_time = data.ending_time
        batch.seats = data.seats
        batch.course_id = data.course_id

        await db.commit()
        await db.refresh(batch)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "msg": "Batch updated successfully"},
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "msg": "Failed to update batch"},
        )
        

async def delete_batch(batch_id : int, current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = result.scalar_one_or_none()

        if not batch:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batch not found"
                }
            )

        await db.delete(batch)
        await db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Batch successfully deleted"
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