from fastapi import APIRouter
from sqlmodel import select
from starlette.requests import Request

from api.deps import SessionDep
from common.execptions import ValidateError
from common.resp import json_data
from models.app import PageInfo, App
from models.user import User

router = APIRouter()


@router.post('/list/page/vo')
def get_app_page(session: SessionDep, request: Request, page_info: PageInfo):
    """
    获取所有 "已过审" APP
    :param session:
    :param request:
    :param page_info:
    :return:
    """
    page_size = page_info.pageSize

    if page_size > 20:
        raise ValidateError('一次仅允许访问不超过20条数据')

    # 找出所以app
    statement = select(App)
    app_objs = session.exec(statement).all()

    # 处理数据，返回
    records = []
    for app in app_objs:
        user_id = app.user_id
        app_dict = app.to_dict()

        # 查询 User 信息
        user_sql = select(User).where(User.id == user_id)
        user_obj = session.exec(user_sql).first()
        if user_obj:
            app_dict['user'] = user_obj.to_dict()

        records.append(app_dict)

    return json_data(data={'records': records}, message='ok')
