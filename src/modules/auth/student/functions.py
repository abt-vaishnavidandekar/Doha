from fastapi import status, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from jose import jwt
from src.configs.env import SECRET_KEY, ALGORITHM
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.student.interface import (
    Create_Student,
    Login_Student,
)
from src.modules.auth.student.models import Student
from src.utils.jwt import create_access_token, create_refresh_token
from src.utils.security import hash_password, verify_password
from src.utils.validations import check_phone, validate_email, validate_password


async def register_student(data: Create_Student, db:AsyncSession):
    try:
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

        result = await db.execute(select(Student).where(Student.ph_no == data.ph_no))
        student = result.scalar_one_or_none()

        if student:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content = {
                    "success" : False,
                    "msg" : "Student with this ph_no already exists"
                }
            )          

        if check_phone(data.ph_no) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "message" : "Invalid phone number : Phone number should be proper 10 digit and starts with [6-9]"
                } 
            )

        if validate_email(data.email) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content ={
                    "success" : False,
                    "msg" : "Enter a valid email format"
                }
            )

        if validate_password(data.password) == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content = {
                    "success" : False,
                    "msg" : "Invalid Password : Password should contain atleast 1 uppercase, lowercase, digit, special character and length should be greater that or equals to 8"
                }
            )

        student = Student(
            first_name=data.first_name,
            last_name=data.last_name,
            age = data.age,
            ph_no = data.ph_no,
            email= data.email,
            password=hash_password(data.password),
        )

        db.add(student)
        await db.commit()
        await db.refresh(student)

        return student

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error": str(e),
            },
    )

    



async def login_student(data : Login_Student, db : AsyncSession):
    
    try:

        result = await db.execute(select(Student).where(Student.email == data.email))

        student = result.scalar_one_or_none()

        if not student:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success" : False,
                    "massage" : "Student with this email not found"
                }
            )
        
        if not verify_password(data.password, student.password):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success" : False,
                    "msg" : "Incorrect or Invalid Password"
                }
            )

       
        
        access_token = create_access_token(user_id = student.id, role = "student")
        refresh_token = create_refresh_token(user_id = student.id, role = "student")

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Successfully LogIn"
            }
        )


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
            path="/",
        )

        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error": str(e),
            },
        )



async def logout(current_user, db:AsyncSession):

    try:
        response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "success" : True,
            "msg" : "Logout Successfully"
        }
        )

        response.delete_cookie(
            key="access_token",
            path="/",
            httponly=True,
            samesite="lax",
        )

        response.delete_cookie(
            key="refresh_token",
            path="/",
            httponly=True,
            samesite="lax",
        )

        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )



def refresh_access_token(refresh_token:Request):
    token = refresh_token.cookies.get('refresh_token')

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        role = payload.get("role")
        token_type = payload.get("type")

        if not user_id or not role or token_type != "refresh":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content = {
                    "success" : False,
                    "msg" : "Invalid Refresh token"
                }
            )

        access_token = create_access_token(user_id=int(user_id), role=role)

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : False,
                "msg" : "Refresh the access token successfully"
            }
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  
            samesite="lax",
            max_age=15 * 60,
            path="/",
        )

        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )