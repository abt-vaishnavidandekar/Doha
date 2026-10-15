from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.role import get_current_student

from src.configs.database import get_db
from src.modules.auth.student.functions import (
    login_student,
    logout,
    register_student,
    refresh_access_token,
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
async def login(data: Login_Student,  db:AsyncSession=Depends(get_db)):
    return await login_student(data=data, db=db)

@student_router.post("/logout")
async def logout(current_user=Depends(get_current_student), db:AsyncSession=Depends(get_db)):
    return await logout()

@student_router.post("/refresh")
async def refresh_the_token(refresh_token : Request):
    return refresh_access_token(refresh_token=refresh_token)