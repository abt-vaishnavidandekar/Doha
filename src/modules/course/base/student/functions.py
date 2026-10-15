import os
import uuid

from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.course.base.admin.interface import Create_Course, Course_Update
from src.modules.course.base.admin.models import Course





async def get_course(current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Course))
        course = result.scalars.all()

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
                "msg" : "Successfully getting the data"
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "courses" : l1
            },
        )