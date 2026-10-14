from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.modules.auth.student.functions import (
    login_student,
    logout_student,
    register_student,
)
from src.modules.auth.student.interface import (
    Create_Student,
    Login_Student,
)

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