from fastapi import APIRouter
from starlette.requests import Request

from common import state
from api.deps import SessionDep
from common.resp import json_data
from models.user import UserCreate, User, UserLogin
from crud import user

router = APIRouter()


@router.post('/register')
def register(session: SessionDep, user_create: UserCreate):
    """ 用户注册
    :param session:
    :param user_create:
    :return: JSONResponse
    """

    user_obj = user.validate_register_info(session, user_create)
    return json_data(data=user_obj.to_dict())


@router.post('/login')
def login(request: Request, session: SessionDep, user_in: UserLogin):
    user_obj = user.validate_login_info(session, user_in)
    request.session['user_login_state'] = user_obj.to_dict()
    return json_data(message="登录成功")


@router.post('/logout')
def logout(request: Request):
    request.session['user_login_state'] = {}
    return json_data(message='退出成功')


@router.get('/get/login')
def get_active_user_login(request: Request):
    """ 获取当前登录用户
    :param request:
    :return: JsonResponse
    """
    user_login_state = request.session.get('user_login_state')
    if not user_login_state:
        return json_data(**{"message": "未登录", "code": state.USER_NOT_LOGIN})
    else:
        return json_data(data=user_login_state)
