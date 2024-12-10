from fastapi import APIRouter, Request
from sqlmodel import select

from api.deps import SessionDep
from common.resp import json_data
from core.score import PickScoreType
from core.utils import generate_id
from crud.user_answer import validate_answer_in, create_user_answer
from models import UserAnswer
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

    # 添加用户答题记录
    answer_obj, app_obj = create_user_answer(session, request, answer_in)

    # 根据不同策略打分
    score_obj = PickScoreType(score_type=app_obj.app_type).choose
    answer_obj_id = score_obj.do_score(app_obj.id, answer_obj, session)

    return json_data(data=answer_obj_id)


@router.get('/get/vo')
def get_each_answer(id: int, session: SessionDep, request: Request):
    """
    展示一个答案
    :param session:
    :param id:
    :param request:
    :return:
    """
    sql = select(UserAnswer).where(UserAnswer.is_delete == False).where(UserAnswer.id == id)
    answer_obj = session.exec(sql).first()
    answer_dict = answer_obj.to_dict()

    user_pub = request.session.get('user_login_state')
    answer_dict.update({'user': user_pub})

    return json_data(data=answer_dict)


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
