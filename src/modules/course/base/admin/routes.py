from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.role import get_current_user
from src.configs.database import get_db
from src.modules.course.base.admin.functions import course_register, get_course
from src.modules.course.base.admin.interface import Create_Course

course_router = APIRouter(tags=["Course"])


@course_router.post("/course_register")
async def course_register_route(
    name: str = Form(...),
    description: str = Form(...),
    overview: str = Form(...),
    document: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):    
    return await course_register(name = name, description=description, overview=overview, document=document, current_user=current_user, db=db)


@course_router.get("/get_courses")
async def get_course_route(current_user = Depends(get_current_user), db:AsyncSession=Depends(get_db)):
    return await get_course(current_user=current_user, db=db)