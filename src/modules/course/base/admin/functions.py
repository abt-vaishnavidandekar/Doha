import os
import uuid

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.course.base.admin.interface import Create_Course, Course_Update
from src.modules.course.base.admin.models import Course

from src.modules.course.base.admin.helpers import UPLOAD_DIR, validate_documents


async def course_register(
    name: str,
    description: str,
    overview: str,
    document : UploadFile,
    current_user,
    db: AsyncSession,
):
    try:

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


        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content = {
                "success" : True,
                "msg" : "Course successfully added"
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


async def get_course(current_user, db:AsyncSession):
    
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


async def update_course(data: Course_Update, current_user, db: AsyncSession, document : UploadFile | None = None):

    try:
        result = await db.execute(select(Course).where(Course.id == data.id))
        course = result.scalar_one_or_none()

        if course is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Course not found"
            }
        )

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(course, field, value)

        await db.commit()
        await db.refresh(course)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success" : False,
                "msg" : "Course successfully updated"
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
    

async def delete_course(course_id : int, current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Course).where(Course.id == course_id))
        course = result.scalar_one_or_none()

        if not course:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "Batch not found"
                }
            )

        await db.delete(course)
        await db.refresh(course)

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content = {
                "success" : True,
                "msg" : "Course successfully deleted"
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