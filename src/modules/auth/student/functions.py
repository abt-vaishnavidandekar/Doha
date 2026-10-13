from src.modules.auth.student.models import Student
from src.modules.auth.student.interface import Create_Student, Update_Student, Login_Student
from fastapi.responses import JSONResponse, Response

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils.jwt import create_access_token, create_refresh_token
from utils.security import hash_password, verify_password
from utils.validations import validate_email, validate_password, check_phone


async def register_student(data: Create_Student, db:AsyncSession):
    result = await db.execute(select(Student).where(Student.email == data.email))
    student = result.scalar_one_or_none()

    if student:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content = {
                "success" : False,
                "msg" : "Student with this email already exists"
            }
        )

    student = Student(
        first_name=data.first_name,
        last_name=data.last_name,
        age = data.age,
        ph_no = check_phone(data.ph_no),
        email=validate_email(data.email),
        password=hash_password(validate_password(data.password)),
    )

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student



async def login_student(data : Login_Student, response : Response, db : AsyncSession):

    result = await db.execute(select(Student).where(Student.email == data.email))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Student with this email not found",
        )
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect or Invalid Password",
        )

    role = "student"
    
    access_token = create_access_token(Student.id, role),
    refresh_token = create_refresh_token(Student.id, role)


    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False, 
        samesite="lax",
        max_age=15 * 60,
        path="/",
    ),
        
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/auth",
    )

    return {"message": "Login successful"}



async def logout_student(response: Response):

    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
    )

    response.delete_cookie(
        key="refresh_token",
        path="/auth",
        httponly=True,
        samesite="lax",
    )

    return {"message": "Logout successful"}