from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.admin.models import Admin
from src.modules.profile.admin.interface import Update_Admin


async def get_admin_detail(user_id: int, db:AsyncSession):
    result = await db.execute(select(Admin).where(Admin.id == user_id))
    admin = result.scalar_one_or_none()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return admin



async def update_admin_datails(data: Update_Admin, db: AsyncSession):

    try: 
        admin_fetch_query = await db.execute(
            select(Admin).where(Admin.id == data.id)
        )
        admin = admin_fetch_query.scalar_one_or_none()
        if not admin:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Admin with this id doesn't exists"
                }
            )


        admin.first_name = data.first_name
        admin.last_name = data.last_name

        await db.commit()

        await db.refresh(admin)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Details updated successfully"
            }
        )

    except:
        import traceback
        traceback.print_exc()
        raise






