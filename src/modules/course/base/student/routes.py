from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.role import get_current_student
from src.configs.database import get_db
from src.modules.course.base.admin.functions import course_register, get_course, update_course, delete_course


course_router = APIRouter(tags=["Course"])


@course_router.get("/get_courses")
async def get_course_route(current_user = Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await get_course(current_user=current_user, db=db)