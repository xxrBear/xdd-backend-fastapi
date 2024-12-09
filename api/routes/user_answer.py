import json

from fastapi import APIRouter, Request
from sqlmodel import select

from api.deps import SessionDep
from common.resp import json_data
from core.utils import generate_id
from crud.user_answer import validate_answer_in
from models import UserAnswer, App
from models.user_answer import UserAnswerIn, UserAnswerDelete

router = APIRouter()


@router.get('/generate/id')
def generate_answer_id():
    """
    自动生成 用户答案 ID
    :return:
    """
    id_ = generate_id()
    return json_data(data=id_)


@router.post('/add')
def add_user_answer(session: SessionDep, request: Request, answer_in: UserAnswerIn):
    """
    添加用户答案
    :param session:
    :param request:
    :param answer_in:
    :return:
    """
    # 参数检验
    validate_answer_in(answer_in, session)

    # 添加进数据库
    app_id = answer_in.appId
    sql = select(App).where(App.id == app_id)
    app_obj = session.exec(sql).first()
    app_dict = app_obj.to_dict()
    app_id = app_dict.pop('id')
    app_dict['appId'] = app_id

    answer_dict = answer_in.to_dict()
    answer_dict.update(app_dict)
    choices = json.dumps(answer_dict['choices'])
    answer_dict['choices'] = choices

    user_pub = request.session.get('user_login_state')
    user_id = user_pub.get('id')
    answer_dict.update({'user_id': user_id, 'user': user_pub})
    answer_obj = UserAnswer(**answer_dict)

    session.add(answer_obj)
    session.commit()
    session.refresh(answer_obj)
    return json_data()


@router.post('/list/page')
def get_all_answer_list(session: SessionDep):
    """
    展示所有答案
    :param session:
    :return:
    """
    sql = select(UserAnswer).where(UserAnswer.is_delete == False)
    answer_objs = session.exec(sql)
    result_list = []
    for answer_obj in answer_objs:
        result_list.append(answer_obj.to_dict())
    return json_data(data={'records': result_list})


@router.post('/my/list/page/vo')
def get_mine_answer_list(session: SessionDep, request: Request):
    user_pub = request.session.get('user_login_state')
    sql = select(UserAnswer).where(UserAnswer.is_delete == False).where(UserAnswer.user_id == user_pub.get('id'))
    answer_objs = session.exec(sql)
    result_list = []
    for answer_obj in answer_objs:
        result_list.append(answer_obj.to_dict())
    return json_data(data={'records': result_list})


@router.post('/delete')
def delete_user_answer(session: SessionDep, user_del: UserAnswerDelete):
    """
    删除答案
    :param session:
    :param user_del:
    :return:
    """
    id_ = user_del.id
    sql = select(UserAnswer).where(UserAnswer.id == id_)
    answer_obj = session.exec(sql).first()
    if answer_obj:
        answer_obj.is_delete = True
        session.commit()
        session.refresh(answer_obj)
    return json_data(data='删除成功')
