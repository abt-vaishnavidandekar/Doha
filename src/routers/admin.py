from modules.auth.admin.routes import admin_router

from fastapi import APIRouter

router = APIRouter(prefix="/admin")

router.include_router(admin_router)
