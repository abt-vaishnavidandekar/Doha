from .models import Admin
from .interface import Create_Admin, Admin_login
from fastapi.responses import JSONResponse, Response

from jose import JWTError, jwt
from src.utils.jwt import ALGORITHM, SECRET_KEY

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils.jwt import create_access_token, create_refresh_token
from utils.security import hash_password, verify_password
from utils.validations import validate_email, validate_password


async def register_admin(data: Create_Admin, db: AsyncSession):
    result = await db.execute(
        select(Admin).where(Admin.email == data.email)
    )
    admin = result.scalar_one_or_none()

    if admin:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content = {
                "success" : False,
                "msg" : "Admin already Exists"
            }
        )

    admin = Admin(
        first_name=data.first_name,
        last_name=data.last_name,
        email=validate_email(data.email),
        password=hash_password(validate_password(data.password)),
    )

    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    return admin


async def login_admin(data : Admin_login, response : Response, db : AsyncSession):

    result = await db.execute(select(Admin).where(Admin.email == data.email))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Admin with this email not found",
        )
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect or Invalid Password",
        )

    role = "admin"
    
    access_token = create_access_token(Admin.id, role)
    refresh_token = create_refresh_token(Admin.id, role)

    print(refresh_token)

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

    return {"message": "Login successful"}



async def logout(response: Response):

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


