import os
import uuid

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.course.base.admin.interface import Create_Course
from src.modules.course.base.admin.models import Course

from .helpers import UPLOAD_DIR, validate_documents


async def course_register(
    name: str,
    description: str,
    overview: str,
    document : UploadFile,
    current_user,
    db: AsyncSession,
):

    result = await db.execute(select(Course).where(Course.name == name))
    course = result.scalar_one_or_none()

    if course:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success" : False,
                "msg" : "Course with this name already exist"
            }
        )

    await validate_documents(document)
    await document.seek(0)

    ext = os.path.splitext(document.filename)[1].lower()
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")

    with open(file_path, "wb") as f:
        f.write(await document.read())

    course = Course(
        name = name,
        description = description,
        overview = overview,
        document = file_path
    )

    db.add(course)
    await db.commit()


    return {"success": True, "msg": "successfully registered"}


async def get_course(current_user, db:AsyncSession):
    result = await db.execute(select(Course))
    course = result.scalar_one_or_none()

    return course
