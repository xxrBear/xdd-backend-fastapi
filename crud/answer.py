import json

from sqlmodel import select
from starlette.requests import Request

from api.deps import SessionDep
from common.execptions import validate_request_exception
from models import UserAnswer, App
from models.answer import UserAnswerIn


def validate_answer_in(user_answer: UserAnswerIn, session: SessionDep):
    """
    验证用户答案参数是否有效
    :param user_answer:
    :param session:
    :return:
    """
    id_ = user_answer.id
    app_id = user_answer.appId

    sql = select(UserAnswer).where(UserAnswer.id == id_)
    answer_obj = session.exec(sql).first()
    validate_request_exception(id_ <= 0 or answer_obj, 'UserAnswer ID 非法')

    sql2 = select(App).where(App.id == app_id)
    app_obj = session.exec(sql2).first()
    validate_request_exception(not app_obj, 'APP ID 非法')


def create_user_answer(session: SessionDep, request: Request, answer_in: UserAnswerIn):
    """
    添加用户答案
    :param session:
    :param request:
    :param answer_in:
    :return:
    """
    # 添加进数据库
    app_id = answer_in.appId
    sql = select(App).where(App.id == app_id)
    app_obj = session.exec(sql).first()
    app_dict = app_obj.to_dict()
    app_dict.pop('id')
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
    return answer_obj, app_obj
