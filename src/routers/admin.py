from fastapi import APIRouter

from modules.auth.admin.routes import admin_router
from modules.batch.base.admin.routes import batch_router
from modules.course.base.admin.routes import course_router
from modules.profile.admin.routes import profile_router
from modules.enrollments.base.admin.routes import enrollment_router

router = APIRouter(prefix="/admin")

router.include_router(admin_router)
router.include_router(course_router)
router.include_router(batch_router)
router.include_router(profile_router)
router.include_router(enrollment_router)
