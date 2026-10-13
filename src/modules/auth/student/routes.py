from src.modules.auth.student.functions import login_student, register_student, logout_student
from sqlalchemy.ext.asyncio import AsyncSession
from src.configs.database import get_db
from fastapi import APIRouter, Depends
from src.modules.auth.student.interface import Create_Student, Update_Student, Login_Student

from fastapi.responses import Response

student_router = APIRouter(tags=["Student"])

@student_router.post("/register")
async def register(data: Create_Student, db:AsyncSession = Depends(get_db)):
    return await register_student(data=data, db=db)

@student_router.post("/login")
async def login(data: Login_Student, response:Response, db:AsyncSession=Depends(get_db)):
    return await login_student(data=data, response=response, db=db)

@student_router.post("/logout")
async def logout(response : Response):
    return await logout_student(response=response)