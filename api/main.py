"""统一注册路由"""
from fastapi import APIRouter

from api.routes import user
from api.routes import app
from api.routes import question
from api.routes import answer
from api.routes import scoring_result

api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(app.router, prefix="/api/app", tags=["app"])
api_router.include_router(question.router, prefix="/api/question", tags=["question"])
api_router.include_router(answer.router, prefix="/api/userAnswer", tags=["userAnswer"])
api_router.include_router(scoring_result.router, prefix="/api/scoringResult", tags=["scoringResult"])
