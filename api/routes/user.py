from urllib import request

from fastapi import APIRouter
from sqlmodel import select
from starlette.requests import Request

from common import state
from api.deps import SessionDep
from common.execptions import ValidateError
from common.resp import json_data
from models.user import UserCreate, User, UserLogin, UserPage, UserDelete
from crud import user

router = APIRouter()


@router.post('/register')
def register(session: SessionDep, user_create: UserCreate):
    """ 用户注册
    :param session:
    :param user_create:
    :return:
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
    :return:
    """
    user_login_state = request.session.get('user_login_state')
    if not user_login_state:
        return json_data(**{"message": "未登录", "code": state.USER_NOT_LOGIN})
    else:
        return json_data(data=user_login_state)


@router.post('/list/page')
def get_all_users(session: SessionDep, user_in: UserPage):
    """ 获取当前所有未删除的用户
    :param session:
    :param user_in:
    :return:
    """
    sql = select(User).where(User.is_delete == False).offset(user_in.current - 1).limit(user_in.pageSize)
    user_objs = session.exec(sql).all()
    return json_data(data={'records': [user.to_dict() for user in user_objs]})


@router.post('/delete')
def get_all_users(session: SessionDep, user_del: UserDelete, request: Request):
    """ 删除用户
    :param session:
    :param user_del:
    :param request:
    :return:
    """
    sql = select(User).where(User.id == user_del.id).where(User.is_delete == False)
    user_obj = session.exec(sql).first()
    if not user_obj:
        raise ValidateError('用户不存在')
    user_obj.is_delete = True
    session.commit()
    session.refresh(user_obj)
    if user_obj.id == request.session.get('user_login_state').get('id'):
        request.session['user_login_state'] = {}
    return json_data(message='删除成功')
