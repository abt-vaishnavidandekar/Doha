from fastapi import Cookie, Depends, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.database import get_db
from src.modules.auth.admin.models import Admin
from src.modules.auth.student.models import Student
from src.utils.jwt import SECRET_KEY, ALGORITHM


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not access_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, 
                     "msg": "Access token Missing"
                     }
                )

    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "access":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"success": False, 
                         "msg": "Invalid access token"
                         }
                    )

        user_id = int(payload["sub"])
        role = payload.get("role")

        if role not in ("student", "admin"):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"success": False, 
                         "msg": "Invalid Role"
                         }
                    )

    except (JWTError, ValueError, KeyError, TypeError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, 
                     "msg": "Invalid or Expired Access token"
                     }
                 )

    model = Admin if role == "admin" else Student

    result = await db.execute(
        select(model).where(model.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, 
                    "msg": "User not found"}
        )

    return user
