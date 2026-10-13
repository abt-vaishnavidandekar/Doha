from src.modules.course.base.admin.models import Course
from src.modules.course.base.admin.interface import Create_Course
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


async def course_register(data: Create_Course, db : AsyncSession):
    result = await db.execute(select).where(Course.name == data.name)
    course = result.scalar_one_or_none()

    if course:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content = {
                "success" : False,
                "msg" : "The same course already exists"
            }
        )

    course = Course(
        name = data.name,
        description = data.description,
        overview = data.overview
    )

    db.add(course)
    await db.commit()
    await db.refresh(course)