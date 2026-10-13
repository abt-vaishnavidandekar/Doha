from modules.auth.student.routes import student_router

from fastapi import APIRouter

router = APIRouter(prefix="/student")

router.include_router(student_router)
