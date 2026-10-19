from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.admin.models import Admin
from src.modules.profile.admin.interface import Update_Admin



async def get_admin_detail(user_id : int, current_user, db: AsyncSession):
    try:
        result = await db.execute(
            select(Admin).where(Admin.id == user_id)
        )
        admin = result.scalar_one_or_none()

        if not admin:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Admin not found"
                }
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content ={
                "success" : True,
                "msg" : "Admin found successfully",
                "admin" : {
                    "first name" : admin.first_name,
                    "last name" : admin.last_name,
                    "email" : admin.email,
                }
            }
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to fetch admin details"
            }
        )




async def update_admin_details(data: Update_Admin, current_user, db: AsyncSession):
    try:
        result = await db.execute(select(Admin).where(Admin.id == data.id))
        admin = result.scalar_one_or_none()

        if not admin:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {
                    "success" : False,
                    "msg" : "User doesn't exists"
                }
            )

        admin.first_name = data.first_name
        admin.last_name = data.last_name

        await db.commit()
        await db.refresh(admin)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Details updated successfully",
            },
        )


    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "success" : False,
                "msg" : "Failed to update admin details"
            }
        )