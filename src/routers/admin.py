from fastapi import APIRouter

from src.modules.auth.admin.routes import admin_router
from src.modules.batch.base.admin.routes import batch_router
from src.modules.course.base.admin.routes import course_router
from src.modules.profile.admin.routes import profile_router
from src.modules.enrollments.base.admin.routes import enrollment_router

router = APIRouter(prefix="/admin")

router.include_router(admin_router)
router.include_router(course_router)
router.include_router(batch_router)
router.include_router(profile_router)
router.include_router(enrollment_router)
