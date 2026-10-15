from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.batch.base.admin.interface import Create_Batch, Update_Batch
from src.modules.batch.base.admin.models import Batch
from src.modules.course.base.admin.models import Course

from src.utils.validations import check_date, check_time



async def get_batch(current_user, db:AsyncSession):
    try:
        result = await db.execute(select(Batch))
        batch = result.scalar_one_or_none()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success": True,
                "msg" : "Data successfully getting",
            },
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential"
            },
        )