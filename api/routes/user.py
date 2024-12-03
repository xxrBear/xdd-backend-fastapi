from fastapi import APIRouter
from starlette.requests import Request

from api.deps import SessionDep
from common.resp import json_data
from common import state
from models.user import UserCreate, User

router = APIRouter()


@router.post('/register')
def register(session: SessionDep, user_create: UserCreate):
    """ 用户注册
    :param session:
    :param user_create:
    :return: JSONResponse
    """
    user_obj = User(**user_create.to_dict())
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    return json_data(data=user_obj.to_dict())


@router.post('/login')
def login():
    return json_data(**{"message": "未登录", "code": state.USER_NOT_LOGIN})


@router.post('/logout')
def logout(request: Request):
    del request.session['user_login_state']
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
