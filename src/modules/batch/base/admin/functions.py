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


        batch = Batch(
            batch_name = data.batch_name,
            startdate = check_date(data.date_field),
            starting_time = check_time(data.starting_time), 
            ending_time = check_time(data.ending_time),
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
                "message": "Invalid Credential"
            },
        )



async def get_batch(current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Batch))
        batch = result.scalar_one_or_none()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True,
                "msg" : "Data successfully getting",
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

async def update_batch(batch_id: int, data: Update_Batch,current_user, db: AsyncSession):

    try:
        result = await db.execute(select(Batch).where(Batch.id == batch_id))
        batch = result.scalar_one_or_none()

        if batch is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Batch not found"
            }
        )

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(batch, field, value)

        await db.commit()
        await db.refresh(batch)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success" : False,
                "msg" : "Batch successfully updated"
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

        db.delete(batch)
        await db.refresh(batch)

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
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