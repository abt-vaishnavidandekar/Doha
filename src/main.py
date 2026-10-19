from fastapi import FastAPI

from src.routers.admin import router as admin_router
from src.routers.student import router as student_router



app = FastAPI(prefix = "/api/v1")

app.include_router(admin_router)
app.include_router(student_router)

@app.get("/")
async def get():
    return {"msg" : "Api is Working"}
