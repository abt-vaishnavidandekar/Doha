from src.modules.auth.admin.models import Admin
from src.modules.auth.admin.interface import Create_Admin, Admin_login, RefreshRequest
from fastapi.responses import JSONResponse, Response
from fastapi import Request

from jose import JWTError, jwt
from src.configs.env import ALGORITHM, SECRET_KEY

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.utils.jwt import create_access_token, create_refresh_token
from src.utils.security import hash_password, verify_password
from src.utils.validations import validate_email, validate_password


async def register_admin(data: Create_Admin, db: AsyncSession):

    try:
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
            

        admin = Admin(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=hash_password(data.password),
        )

        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Admin successfully Registered"
            },         
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )
    


async def login_admin(data : Admin_login, db : AsyncSession):
    try:

        result = await db.execute(select(Admin).where(Admin.email == data.email))

        admin = result.scalar_one_or_none()

        if not admin:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success" : False,
                    "massage" : "Admin with this email not found"
                }
            )
        
        if not verify_password(data.password, admin.password):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success" : False,
                    "msg" : "Incorrect or Invalid Password"
                }
            )


        access_token = create_access_token(user_id = admin.id, role = "admin")
        refresh_token = create_refresh_token(user_id = admin.id, role = "admin")

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Successfully regitered"
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
                "message": "Internal Server Error",
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
            path="/auth",
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
                "success" : True,
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