from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.batch.base.admin.interface import Create_Batch, Update_Batch
from src.modules.batch.base.admin.models import Batch
from src.modules.course.base.admin.models import Course

from src.utils.validations import check_date, check_time


async def create_batch(data: Create_Batch, current_user, db:AsyncSession):
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
        date_field = check_date(data.date_field),
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




async def get_batch(current_user, db:AsyncSession):
    result = await db.execute(select(Batch))
    batch = result.scalar_one_or_none()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "success": True,
            "msg" : "Data successfully updated",
        },
    )


async def update_batch(batch_id:int, current_user, data:Update_Batch, db:AsyncSession):

    result = await db.execute(select(Batch).where(Batch.id==batch_id))
    batch = result.scalar_one_or_none()

    if not batch:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success" :False,
                "msg" : "Batch with this id doesn't exists"
            }
        )

    update_data = data.model_dump(exclude_unset=True)


    for key, value in update_data.items():
        setattr(batch, key, value)


    await db.commit()
    await db.refresh(batch)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "success": True,
            "msg" : "Data successfully updated"
                    
        }
    )