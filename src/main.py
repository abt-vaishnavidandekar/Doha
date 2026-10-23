from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.configs.redis import close_redis

from src.routers.admin import router as admin_router
from src.routers.student import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_redis()



app = FastAPI(lifespan=lifespan)

app.include_router(admin_router)
app.include_router(student_router)

@app.get("/")
async def get():
    return JSONResponse(
        status_code= status.HTTP_200_OK,
        content={
            "success" : True,
            "msg" : "Api is Working"
        }
    )

