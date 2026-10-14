from fastapi import APIRouter

from modules.auth.student.routes import student_router
from src.modules.profile.student.routes import profile_router
from src.modules.enrollments.base.student.routes import enrollment_router

router = APIRouter(prefix="/student")

router.include_router(student_router)
router.include_router(profile_router)
router.include_router(enrollment_router)
