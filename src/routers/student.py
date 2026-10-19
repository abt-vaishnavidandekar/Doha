from fastapi import APIRouter

from src.modules.auth.student.routes import student_router
from src.modules.profile.student.routes import profile_router
from src.modules.course.base.student.routes import course_router
from src.modules.batch.base.student.routes import batch_router
from src.modules.enrollments.base.student.routes import enrollment_router

router = APIRouter(prefix="/student")

router.include_router(student_router)
router.include_router(course_router)
router.include_router(batch_router)
router.include_router(profile_router)
router.include_router(enrollment_router)