from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.role import get_current_admin
from src.configs.database import get_db
from src.modules.course.base.admin.functions import course_register, get_course, update_course, delete_course
from src.modules.course.base.admin.interface import Create_Course, Course_Update

course_router = APIRouter(tags=["Course"])

@course_router.post("/course_register")
async def course_register_route(
    name: str = Form(...),
    description: str = Form(...),
    overview: str = Form(...),
    document: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin)
):    
    return await course_register(name = name, description=description, overview=overview, document=document, current_user=current_user, db=db)


@course_router.get("/courses")
async def get_course_route(current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await get_course(current_user=current_user, db=db)


@course_router.delete("/course/{course_id}")
async def delete_course_route(course_id:int, current_user = Depends(get_current_admin), db:AsyncSession=Depends(get_db)):
    return await delete_course(course_id=course_id, current_user=current_user, db=db)


@course_router.put("/course/{course_id}")
async def update(
    course_id : int,
    data : Course_Update | None = Form(default=None),
    document : UploadFile | None = File(default=None),
    current_user=Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):

    return await update_course(
        course_id=course_id,
        data=data,
        document=document,
        current_user=current_user,
        db=db,
    )