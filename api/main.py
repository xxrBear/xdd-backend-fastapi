"""统一注册路由"""
from fastapi import APIRouter

from api.routes import user
from api.routes import app
from api.routes import question

api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(app.router, prefix="/api/app", tags=["app"])
api_router.include_router(question.router, prefix="/api/question", tags=["question"])
