from fastapi import APIRouter
from sqlmodel import select
from starlette.requests import Request

from api.deps import SessionDep
from common import state
from common.resp import json_data
from core.utils import adapter_records_info
from crud import user
from crud.user import delete_user_by_id
from models.user import UserCreate, User, UserLogin, UserPage, UserDelete

router = APIRouter()


@router.post('/register')
async def register(session: SessionDep, user_create: UserCreate):
    """ 用户注册
    :param session:
    :param user_create:
    :return:
    """
    user_obj = user.validate_register_info(session, user_create)
    return json_data(data=user_obj.to_dict())


@router.post('/login')
async def login(request: Request, session: SessionDep, user_in: UserLogin):
    user_obj = user.validate_login_info(session, user_in)
    request.session['user_login_state'] = user_obj.to_dict()
    return json_data(message="登录成功")


@router.post('/logout')
async def logout(request: Request):
    request.session['user_login_state'] = {}
    return json_data(message='退出成功')


@router.get('/get/login')
async def get_active_user_login(request: Request):
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
async def get_all_users(session: SessionDep, user_in: UserPage):
    """ 获取当前所有未删除的用户
    :param session:
    :param user_in:
    :return:
    """
    sql = select(User).where(User.is_delete == False).offset(user_in.current - 1).limit(user_in.pageSize)

    if user_in.userName:
        sql = sql.where(User.user_name.like('%{}%'.format(user_in.userName)))
    if user_in.userProfile:
        sql = sql.where(User.user_profile.like('%{}%'.format(user_in.userProfile)))
    user_objs = session.exec(sql).all()
    data = adapter_records_info(user_objs, user_in.pageSize)
    data.update({'records': [user.to_dict() for user in user_objs]})
    return json_data(data=data)


@router.post('/delete')
async def delete_all_users(session: SessionDep, user_del: UserDelete, request: Request):
    """ 删除用户
    :param session:
    :param user_del:
    :param request:
    :return:
    """
    result = delete_user_by_id(session, user_del, request)
    return result
